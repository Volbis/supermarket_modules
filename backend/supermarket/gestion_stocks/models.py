from django.db import models
from django.utils import timezone

# Create your models here.


# la classe produit 

class Produit(models.Model):
      id_product = models.UUIDField(primary_key=True, editable=False)
      nom = models.CharField(max_length=255)
      reference = models.CharField(max_length=255, unique=True)
      designation = models.TextField(max_length=500)
      prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
      quantite_en_stock  = models.IntegerField()
      seuil_de_reapprovisionnement = models.IntegerField()
      date_de_peremption = models.DateField()
      categorie = models.ForeignKey('Categorie', on_delete=models.CASCADE)
      fournisseur = models.ForeignKey('Fournisseur', on_delete=models.CASCADE)

      def estSousSeuil(self):
            return self.quantite_en_stock < self.seuil_de_reapprovisionnement
      def atteintSeuil(self):
            return self.quantite_en_stock == self.seuil_de_reapprovisionnement
      def incrementerStock(self, quantite):
            self.quantite_en_stock += quantite
            self.save()
      def decrementerStock(self, quantite):
            self.quantite_en_stock -= quantite
            self.save()
      def estPerime(self):
            return self.date_de_peremption < timezone.now().date()
      
      def __str__(self):
            return super().__str__() + f" - {self.nom} ({self.reference})"
      

class Categorie(models.Model): 

      TYPE_CHOICES = [
            ('BOISSON', 'Boisson'),
            ('FRUIT', 'Fruit'),
            ('LEGUME', 'Légume'),
            ('EPICERIE', 'Épicerie'),
            ('VIANDE', 'Viande'),
            ('POISSON', 'Poisson'),
            ('PRODUIT_LAITIER', 'Produit laitier'),
            ('ELECTRONIQUE', 'Électronique'),
            ('HABILLEMENT', 'Habillement'),
            ('JOUET', 'Jouet'),
            ('JEUX_VIDEO', 'Jeux vidéo'),
            ('AUTRE', 'Autre')
      ]
      id_categorie = models.UUIDField(primary_key=True, editable=False)
      nom = models.CharField(max_length=255, choices=TYPE_CHOICES)
      description = models.TextField(max_length=500, null=True, blank=True)


      def getProduits(self):
            return Produit.objects.filter(categorie=self)
      
      def __str__(self):
            return super().__str__() + f" - {self.nom}"
      


class Stock(models.Model):
      id_stock = models.UUIDField(primary_key=True, editable=False)
      produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
      quantite = models.IntegerField()
      date_ajout = models.DateTimeField(auto_now_add=True)
      date_modification = models.DateTimeField(auto_now=True)

      def __str__(self):
            return super().__str__() + f" - {self.produit.nom} : {self.quantite}"
      
      def verifierDisponibilite(self, p: Produit):
            return self.quantite >= p.quantite_en_stock
      def ajouterStock(self, quantite):
            self.quantite += quantite
            self.save()
      def retirerStock(self, quantite):
            if quantite > self.quantite:
                  raise ValueError("Quantité insuffisante en stock")
                  return self.quantite
            self.quantite -= quantite
            self.save()
      
      def quantiteDisponible(self):
            return self.quantite
      
      
class Fournisseur(models.Model):
      id_fournisseur = models.UUIDField(primary_key=True, editable=False)
      nom = models.CharField(max_length=255)
      contact = models.CharField(max_length=255)
      adresse = models.TextField(max_length=500)
      catalogue_produits = models.TextField(max_length=1000, null=True, blank=True)
      delais_livraison_jours = models.IntegerField()

      def getProduitsFournis(self):
            return Produit.objects.filter(fournisseur=self)
      def obtenirPrixProduit(self, produit: Produit):
            if produit.fournisseur != self:
                  raise ValueError("Le produit n'est pas fourni par ce fournisseur")
            return produit.prix_unitaire
      

      def __str__(self):
            return super().__str__() + f" - {self.nom}"
      
class CommandeApprovisionnement(models.Model):
      TYPE_STATUT = [
            ('EN_COURS', 'En cours'),
            ('LIVREE', 'Livrée'),
            ('ANNULEE', 'Annulée')
      ]

      id_commande = models.UUIDField(primary_key=True, editable=False)
      fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)
      date_commande = models.DateTimeField(auto_now_add=True)
      date_livraison_prevue = models.DateTimeField()
      statut = models.CharField(max_length=50, choices=TYPE_STATUT, default='EN_COURS')

      def __str__(self):
            return super().__str__() + f" - Commande {self.id_commande} chez {self.fournisseur.nom}"
      
      def calculerMotantTotal(self):
            details = DetailCommande.objects.filter(commande=self)
            total = sum([detail.produit.prix_unitaire * detail.quantite for detail in details])
            return total
      
      def valider(self):
            self.statut = 'LIVREE'
            self.save()
      def annuler(self):
            self.statut = 'ANNULEE'
            self.save()

class DetailCommande(models.Model):
      id_detail = models.UUIDField(primary_key=True, editable=False)
      commande = models.ForeignKey(CommandeApprovisionnement, on_delete=models.CASCADE)
      produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
      quantite = models.IntegerField()

      def __str__(self):
            return super().__str__() + f" - {self.produit.nom} x {self.quantite} pour commande {self.commande.id_commande}"
      
      def calculerSousTotal(self):
            return self.produit.prix_unitaire * self.quantite


class AlertStock(models.Model):
      id_alert = models.UUIDField(primary_key=True, editable=False)
      produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
      message = models.TextField(max_length=500)
      date_creation = models.DateTimeField(auto_now_add=True)

      def __str__(self):
            return super().__str__() + f" - Alert for {self.produit.nom}"


class HistoriqueStock(models.Model):
      id_historique = models.UUIDField(primary_key=True, editable=False)
      produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
      quantite_modifiee = models.IntegerField()
      date_modification = models.DateTimeField(auto_now_add=True)
      type_modification = models.CharField(max_length=50)  # 'AJOUT' ou 'RETRAIT'

      def __str__(self):
            return super().__str__() + f" - {self.type_modification} de {self.quantite_modifiee} pour {self.produit.nom}"

class ResponsableStock(models.Model):
      id_responsable = models.UUIDField(primary_key=True, editable=False)
      nom = models.CharField(max_length=255)
      email = models.EmailField(unique=True)
      telephone = models.CharField(max_length=20)

      def __str__(self):
            return super().__str__() + f" - {self.nom} ({self.email})"
      
      def validerCommande(self, commande: CommandeApprovisionnement):
            commande.valider()

      def consulterRapportInventaire(self):
            produits = Produit.objects.all()
            rapport = []
            for produit in produits:
                  rapport.append({
                        'produit': produit.nom,
                        'quantite_en_stock': produit.quantite_en_stock,
                        'seuil_de_reapprovisionnement': produit.seuil_de_reapprovisionnement,
                        'est_sous_seuil': produit.estSousSeuil(),
                        'est_perime': produit.estPerime()
                  })
            return rapport
      
class HistoriqueVente(models.Model):
      id_historique_vente = models.UUIDField(primary_key=True, editable=False)
      produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
      quantite_vendue = models.IntegerField()
      date_vente = models.DateTimeField(auto_now_add=True)
      montant_total = models.DecimalField(max_digits=10, decimal_places=2)
      chiffre_affaires_journalier = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

      def __str__(self):
            return super().__str__() + f" - Vente de {self.quantite_vendue} de {self.produit.nom} pour {self.montant_total}"
      
      def calculerTendanceVente(self):
            # Placeholder pour une logique de tendance plus complexe
            return "Tendance stable"
      
      def prevoirDemande(self):
            # Placeholder pour une logique de prévision plus complexe
            return self.quantite_vendue * 1.1  # Prévision simple : 10% d'augmentation