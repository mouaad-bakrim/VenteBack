from django.db import models
from django.utils import timezone

class Devis(models.Model):
    # Statut du devis (par exemple, en attente, accepté, refusé)
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('accepte', 'Accepté'),
        ('refuse', 'Refusé'),
        ('annule', 'Annulé'),
    ]

    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='devis', verbose_name="Client")
    date_creation = models.DateTimeField(default=timezone.now, verbose_name="Date de création")
    date_limite = models.DateTimeField(null=True, blank=True, verbose_name="Date limite de validité")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente', verbose_name="Statut du devis")
    montant_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant total estimé")
    remise = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Remise (%)")
    taxes = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Taxe (%)")

    def __str__(self):
        return f"Devis #{self.id} - {self.client.nom}"

    class Meta:
        verbose_name = "Devis"
        verbose_name_plural = "Devis"

class DevisLigne(models.Model):
    devis = models.ForeignKey('Devis', on_delete=models.CASCADE, related_name='lignes', verbose_name="Devis")
    produit = models.ForeignKey('Produit', on_delete=models.CASCADE, related_name='lignes_devis', verbose_name="Produit")
    article = models.ForeignKey('ArticleSite', on_delete=models.CASCADE, related_name='lignes_devis', verbose_name="Article")
    quantite = models.PositiveIntegerField(verbose_name="Quantité")
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix unitaire")
    remise = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Remise (%)")
    montant_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant total")

    def __str__(self):
        return f"Ligne Devis #{self.id} - {self.produit.nom}"

    def save(self, *args, **kwargs):
        # Calcul du montant total après remise
        self.montant_total = self.quantite * self.prix_unitaire * (1 - self.remise / 100)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Ligne Devis"
        verbose_name_plural = "Lignes Devis"





class BonCommande(models.Model):
    devis = models.ForeignKey('Devis', on_delete=models.CASCADE, related_name='bons_commande', verbose_name="Devis")
    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='bons_commande', verbose_name="Client")
    date_commande = models.DateTimeField(default=timezone.now, verbose_name="Date de commande")
    statut = models.CharField(max_length=20, choices=Devis.STATUT_CHOICES, default='en_attente', verbose_name="Statut de la commande")
    montant_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant total de la commande")
    mode_paiement = models.CharField(max_length=50, verbose_name="Mode de paiement")
    date_livraison = models.DateTimeField(null=True, blank=True, verbose_name="Date de livraison")

    def __str__(self):
        return f"Bon de Commande #{self.id} - {self.client.nom}"

    class Meta:
        verbose_name = "Bon de Commande"
        verbose_name_plural = "Bons de Commandes"
class BonCommandeLigne(models.Model):
    bon_commande = models.ForeignKey('BonCommande', on_delete=models.CASCADE, related_name='lignes', verbose_name="Bon de Commande")
    produit = models.ForeignKey('Produit', on_delete=models.CASCADE, related_name='lignes_bon_commande', verbose_name="Produit")
    article = models.ForeignKey('ArticleSite', on_delete=models.CASCADE, related_name='lignes_bon_commande', verbose_name="Article")
    quantite = models.PositiveIntegerField(verbose_name="Quantité")
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix unitaire")
    montant_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant total")

    def __str__(self):
        return f"Ligne Bon de Commande #{self.id} - {self.produit.nom}"

    def save(self, *args, **kwargs):
        # Calcul du montant total
        self.montant_total = self.quantite * self.prix_unitaire
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Ligne Bon de Commande"
        verbose_name_plural = "Lignes Bons de Commande"





class BonLivraison(models.Model):
    bon_commande = models.ForeignKey('BonCommande', on_delete=models.CASCADE, related_name='bons_livraison', verbose_name="Bon de commande")
    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='bons_livraison', verbose_name="Client")
    date_livraison = models.DateTimeField(default=timezone.now, verbose_name="Date de livraison")
    statut = models.CharField(max_length=20, choices=[('livre', 'Livré'), ('en_cours', 'En cours'), ('annule', 'Annulé')], default='en_cours', verbose_name="Statut de livraison")
    adresse_livraison = models.CharField(max_length=255, verbose_name="Adresse de livraison")

    def __str__(self):
        return f"Bon de Livraison #{self.id} - {self.client.nom}"

    class Meta:
        verbose_name = "Bon de Livraison"
        verbose_name_plural = "Bons de Livraison"

class BonLivraisonLigne(models.Model):
    bon_livraison = models.ForeignKey('BonLivraison', on_delete=models.CASCADE, related_name='lignes', verbose_name="Bon de Livraison")
    produit = models.ForeignKey('Produit', on_delete=models.CASCADE, related_name='lignes_bon_livraison', verbose_name="Produit")
    article = models.ForeignKey('ArticleSite', on_delete=models.CASCADE, related_name='lignes_bon_livraison', verbose_name="Article")
    quantite = models.PositiveIntegerField(verbose_name="Quantité")
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix unitaire")
    montant_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant total")

    def __str__(self):
        return f"Ligne Bon de Livraison #{self.id} - {self.produit.nom}"

    def save(self, *args, **kwargs):
        # Calcul du montant total
        self.montant_total = self.quantite * self.prix_unitaire
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Ligne Bon de Livraison"
        verbose_name_plural = "Lignes Bons de Livraison"


from django.db import models
from django.utils import timezone


class Facture(models.Model):
    class Meta:
        verbose_name = "Facture"
        verbose_name_plural = "Factures"

    bon_commande = models.ForeignKey('BonCommande', on_delete=models.CASCADE, related_name='factures',
                                     verbose_name="Bon de commande")
    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='factures', verbose_name="Client")
    date_facture = models.DateTimeField(default=timezone.now, verbose_name="Date de la facture")
    montant_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant total de la facture")
    montant_taxe = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant des taxes")
    montant_remise = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Remise appliquée")
    statut_paiement = models.CharField(max_length=20,
                                       choices=[('en_attente', 'En attente'), ('paye', 'Payé'), ('annule', 'Annulé')],
                                       default='en_attente', verbose_name="Statut de paiement")
    mode_paiement = models.CharField(max_length=50, verbose_name="Mode de paiement")
    date_limite_paiement = models.DateTimeField(null=True, blank=True, verbose_name="Date limite de paiement")
    date_paiement_effectif = models.DateTimeField(null=True, blank=True, verbose_name="Date de paiement effectif")
    numero_facture = models.CharField(max_length=100, unique=True, verbose_name="Numéro de facture")
    conditions_paiement = models.TextField(blank=True, null=True, verbose_name="Conditions de paiement")
    adresse_livraison = models.TextField(blank=True, null=True, verbose_name="Adresse de livraison")
    statut_expedition = models.CharField(max_length=20, choices=[('en_attente', 'En attente'), ('expedie', 'Expédiée'),
                                                                 ('livree', 'Livrée')], default='en_attente',
                                         verbose_name="Statut d'expédition")

    paiement_partiel = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                           verbose_name="Montant payé jusqu'à présent")
    paiement_restant = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                           verbose_name="Montant restant à payer")

    statut_facturation = models.CharField(max_length=20,
                                          choices=[('en_cours', 'En cours'), ('facture_finale', 'Facture finale'),
                                                   ('proforma', 'Proforma')], default='en_cours',
                                          verbose_name="Statut de la facturation")

    def __str__(self):
        return f"Facture #{self.numero_facture} - {self.client.nom}"

    def save(self, *args, **kwargs):
        # Calcul automatique du montant restant à payer et des taxes
        self.montant_taxe = (self.montant_total - self.montant_remise) * 0.2  # Exemple de calcul pour une taxe de 20%
        self.paiement_restant = self.montant_total - self.paiement_partiel
        super().save(*args, **kwargs)

    @property
    def is_paid(self):
        return self.paiement_restant == 0

    @property
    def is_overdue(self):
        # Vérifier si la date limite de paiement est passée et que le paiement n'a pas été effectué
        if self.date_limite_paiement and self.paiement_restant > 0 and timezone.now() > self.date_limite_paiement:
            return True
        return False



