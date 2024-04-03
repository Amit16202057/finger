from django.shortcuts import render, redirect
from .models import Attendance
from pyfingerprint.pyfingerprint import PyFingerprint

def index(request):
    return render(request, 'index.html')

def enroll(request):
    if request.method == 'POST':
        name = request.POST['name']

        fingerprint_sensor = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        try:
            if not fingerprint_sensor.verifyPassword():
                raise ValueError('The given fingerprint sensor password is wrong!')
        except Exception as e:
            return render(request, 'index.html', {'error_message': 'Error initializing the fingerprint sensor: ' + str(e)})

        try:
            fingerprint_sensor.readImage()
            fingerprint_sensor.convertImage(0x01)
            result = fingerprint_sensor.searchTemplate()
            fingerprint_template = fingerprint_sensor.downloadCharacteristics(0x01)

            Attendance.objects.create(name=name, fingerprint_template=fingerprint_template)

            return redirect('index')
        except Exception as e:
            return render(request, 'index.html', {'error_message': 'Error enrolling fingerprint: ' + str(e)})

def verify(request):
    if request.method == 'POST':
        fingerprint_sensor = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        try:
            if not fingerprint_sensor.verifyPassword():
                raise ValueError('The given fingerprint sensor password is wrong!')
        except Exception as e:
            return render(request, 'index.html', {'error_message': 'Error initializing the fingerprint sensor: ' + str(e)})

        try:
            fingerprint_sensor.readImage()
            fingerprint_sensor.convertImage(0x01)
            result = fingerprint_sensor.searchTemplate()
            fingerprint_template = fingerprint_sensor.downloadCharacteristics(0x01)

            match = Attendance.objects.filter(fingerprint_template=fingerprint_template).first()

            if match:
                return render(request, 'index.html', {'result_message': 'Fingerprint recognized for: ' + match.name})
            else:
                return render(request, 'index.html', {'result_message': 'Fingerprint not recognized.'})
        except Exception as e:
            return render(request, 'index.html', {'error_message': 'Error verifying fingerprint: ' + str(e)})
