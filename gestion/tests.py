from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from evaluacion.models import Examen, Resultado
from datetime import date

User = get_user_model()


class SistemaTest(TestCase):

    def setUp(self):
        self.client = Client()

        self.admin = User.objects.create_user(
            username="admin",
            password="1234",
            is_staff=True,
            rol="ADMIN"
        )

        self.candidato = User.objects.create_user(
            username="candidato",
            password="1234",
            rol="CANDIDATO"
        )

    # CP-01 Acceso a examen sin login (cubre puerta trasera)
    def test_acceso_examen_sin_login(self):
        response = self.client.get(reverse('presentar_examen'))
        self.assertEqual(response.status_code, 302)

    # CP-02 Login correcto
    def test_login_usuario(self):
        response = self.client.post(reverse('login'), {
            "username": "admin",
            "password": "1234"
        })
        self.assertEqual(response.status_code, 302)

    # CP-03 Acceso al examen con login
    def test_acceso_examen_con_login(self):
        self.client.login(username="candidato", password="1234")
        response = self.client.get(reverse('presentar_examen'))
        self.assertEqual(response.status_code, 302)

    # CP-04 Acceso al panel admin sin permisos (cubre puerta trasera)
    def test_panel_admin_sin_staff(self):
        self.client.login(username="candidato", password="1234")
        response = self.client.get(reverse('panel_admin'))
        self.assertNotEqual(response.status_code, 200)

    # CP-05 Acceso al login
    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    # CP-06 Acceso al panel candidato
    def test_panel_candidato(self):
        self.client.login(username="candidato", password="1234")
        response = self.client.get(reverse('panel_candidato'))
        self.assertIn(response.status_code, [200, 302])

    # CP-07 Logout
    def test_logout(self):
        self.client.login(username="candidato", password="1234")
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    # CP-08 Examen inexistente redirige
    def test_examen_no_existe(self):
        self.client.login(username="candidato", password="1234")
        response = self.client.get(reverse('presentar_examen'))
        self.assertEqual(response.status_code, 302)

    # CP-09 Usuario ya presentó el examen
    def test_usuario_ya_presento_examen(self):
        self.client.login(username="candidato", password="1234")

        examen = Examen.objects.create(
            titulo="Examen Test",
            fecha=date.today()
        )

        Resultado.objects.create(
            usuario=self.candidato,
            examen=examen,
            puntaje=5
        )

        response = self.client.get(reverse('presentar_examen'))
        self.assertEqual(response.status_code, 302)

    # CP-10 Ver examen (GET)
    def test_ver_examen(self):
        self.client.login(username="candidato", password="1234")

        Examen.objects.create(
            titulo="Examen Test",
            fecha=date.today()
        )

        response = self.client.get(reverse('presentar_examen'))
        self.assertEqual(response.status_code, 200)

    # CP-11 Responder examen (POST)
    def test_responder_examen(self):
        self.client.login(username="candidato", password="1234")

        Examen.objects.create(
            titulo="Examen Test",
            fecha=date.today()
        )

        response = self.client.post(reverse('presentar_examen'), {})
        self.assertEqual(response.status_code, 302)

    def test_login_incorrecto(self):

        response = self.client.post(reverse('login'), {
            "username": "admin",
            "password": "incorrecta"
        })

        self.assertEqual(response.status_code, 200)

    
    def test_admin_crear_usuario_existente(self):

        self.client.login(username="admin", password="1234")

        response = self.client.post(reverse('panel_admin'), {
            "username": "candidato",  # ya existe
            "password": "1234",
            "email": "test@test.com",
            "cedula": "123"
        })

        self.assertEqual(response.status_code, 200)


    #(cubre puerta trasera)
    def test_admin_no_puede_ver_panel_candidato(self):

        self.client.login(username="admin", password="1234")

        response = self.client.get(reverse('panel_candidato'))

        self.assertEqual(response.status_code, 302)







