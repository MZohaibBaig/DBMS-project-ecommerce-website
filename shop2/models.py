from django.db import models


class Product(models.Model):
    # Columns from lenshive.sql -> pythonic names with db_column mappings
    product_id = models.AutoField(primary_key=True, db_column="ProductID")
    name = models.CharField(max_length=150, db_column="Name")
    description = models.TextField(null=True, blank=True, db_column="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, db_column="Price")
    stock_quantity = models.IntegerField(default=0, db_column="StockQuantity")
    image_url = models.CharField(max_length=255, null=True, blank=True, db_column="ImageURL")
    style = models.CharField(max_length=50, null=True, blank=True, db_column="Style")
    material = models.CharField(max_length=50, null=True, blank=True, db_column="Material")
    ar_model_url = models.CharField(max_length=255, null=True, blank=True, db_column="ARModelURL")

    emb1 = models.FloatField(null=True, blank=True, db_column="emb1")
    emb2 = models.FloatField(null=True, blank=True, db_column="emb2")
    emb3 = models.FloatField(null=True, blank=True, db_column="emb3")
    emb4 = models.FloatField(null=True, blank=True, db_column="emb4")
    emb5 = models.FloatField(null=True, blank=True, db_column="emb5")

    # These are populated by MySQL defaults/trigger-like behavior; keep nullable in Django
    created_at = models.DateTimeField(null=True, blank=True, db_column="CreatedAt")
    updated_at = models.DateTimeField(null=True, blank=True, db_column="UpdatedAt")

    class Meta:
        db_table = "products"
        managed = False  # keep Django from managing this table
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["-created_at"]  # default ordering if you use Product.objects.all()

    def __str__(self):
        return f"{self.name} (#{self.product_id})"


class CartItem(models.Model):
    cart_item_id = models.AutoField(primary_key=True, db_column="CartItemID")
    cart_id = models.IntegerField(db_column="CartID")
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        db_column="ProductID",
        related_name="cartitems",
    )
    quantity = models.IntegerField(default=1, db_column="Quantity")

    class Meta:
        db_table = "cartitems"
        managed = False
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
