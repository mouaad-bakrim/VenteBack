from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Client(models.Model):
    class TypeClient(models.TextChoices):
        PARTICULIER = 'P', 'Particulier'
        ENTREPRISE = 'E', 'Entreprise'

    # Champs de base
    nom = models.CharField(max_length=200, verbose_name="Nom du client")
    email = models.EmailField(unique=True, verbose_name="Email")
    telephone = models.CharField(
        max_length=20,
        verbose_name="Numéro de téléphone",
        blank=True,
        null=True,
        validators=[RegexValidator(r'^\+?\d{10,15}$', 'Numéro de téléphone invalide')]
    )
    type_client = models.CharField(
        max_length=1,
        choices=TypeClient.choices,
        default=TypeClient.PARTICULIER,
        verbose_name="Type de client"
    )
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création du client")
    statut = models.BooleanField(default=True, verbose_name="Client actif")
    site = models.ForeignKey('Site', on_delete=models.SET_NULL, null=True, related_name='clients', verbose_name="Site client")

    # Informations spécifiques pour entreprise
    entreprise_nom = models.CharField(max_length=255, verbose_name="Nom de l'entreprise", blank=True, null=True)
    SIRET = models.CharField(max_length=14, verbose_name="Numéro SIRET", blank=True, null=True)
    num_tva = models.CharField(max_length=20, verbose_name="Numéro de TVA", blank=True, null=True)

    # Relation avec utilisateur (si vous avez un modèle d'utilisateur Django personnalisé ou un profil)
    utilisateur = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Utilisateur lié")

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def clean(self):
        if self.type_client == self.TypeClient.ENTREPRISE:
            if not self.SIRET or not self.num_tva:
                raise ValidationError(_("Le numéro SIRET et le numéro de TVA sont requis pour les entreprises."))
        else:
            if self.SIRET or self.num_tva:
                raise ValidationError(_("Les numéros SIRET et de TVA ne sont pas nécessaires pour un particulier."))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
