# This is a refined Django model module based on your existing database.
from django.db import models

# Foundational models (no dependencies on other models in this file)
class Users(models.Model):
    user_id = models.AutoField(db_column='UserID', primary_key=True)
    name = models.CharField(db_column='Name', max_length=100)
    email = models.CharField(db_column='Email', unique=True, max_length=150)
    password_hash = models.CharField(db_column='PasswordHash', max_length=255)
    role = models.CharField(db_column='Role', max_length=8, blank=True, null=True)
    phone_number = models.CharField(db_column='PhoneNumber', max_length=30, blank=True, null=True)
    address = models.TextField(db_column='Address', blank=True, null=True)
    is_active = models.BooleanField(db_column='IsActive', default=True)
    created_at = models.DateTimeField(db_column='CreatedAt', auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(db_column='UpdatedAt', auto_now=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'

    def __str__(self):
        return self.name

class Products(models.Model):
    product_id = models.AutoField(db_column='ProductID', primary_key=True)
    name = models.CharField(db_column='Name', max_length=150)
    description = models.TextField(db_column='Description', blank=True, null=True)
    price = models.DecimalField(db_column='Price', max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(db_column='StockQuantity')
    image_url = models.CharField(db_column='ImageURL', max_length=255, blank=True, null=True)
    style = models.CharField(db_column='Style', max_length=50, blank=True, null=True)
    material = models.CharField(db_column='Material', max_length=50, blank=True, null=True)
    ar_model_url = models.CharField(db_column='ARModelURL', max_length=255, blank=True, null=True)
    emb1 = models.FloatField(blank=True, null=True)
    emb2 = models.FloatField(blank=True, null=True)
    emb3 = models.FloatField(blank=True, null=True)
    emb4 = models.FloatField(blank=True, null=True)
    emb5 = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(db_column='CreatedAt', auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(db_column='UpdatedAt', auto_now=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'products'

    def __str__(self):
        return self.name

class Lenstypes(models.Model):
    lens_type_id = models.AutoField(db_column='LensTypeID', primary_key=True)
    name = models.CharField(db_column='Name', max_length=100)
    description = models.TextField(db_column='Description', blank=True, null=True)
    uv_protection = models.BooleanField(db_column='UVProtection', default=False)
    blue_light_blocking = models.BooleanField(db_column='BlueLightBlocking', default=False)
    transition = models.BooleanField(db_column='Transition', default=False)
    created_at = models.DateTimeField(db_column='CreatedAt', auto_now_add=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lenstypes'

    def __str__(self):
        return self.name

class Staticpages(models.Model):
    page_id = models.AutoField(db_column='PageID', primary_key=True)
    slug = models.CharField(db_column='Slug', unique=True, max_length=100, blank=True, null=True)
    title = models.CharField(db_column='Title', max_length=200, blank=True, null=True)
    content = models.TextField(db_column='Content', blank=True, null=True)
    updated_at = models.DateTimeField(db_column='UpdatedAt', auto_now=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'staticpages'
    
    def __str__(self):
        return self.title


# Dependent models
class Adminstaff(models.Model):
    staff_id = models.AutoField(db_column='StaffID', primary_key=True)
    user = models.OneToOneField(Users, on_delete=models.CASCADE, db_column='UserID')
    permissions_role = models.CharField(db_column='PermissionsRole', max_length=100, blank=True, null=True)
    hire_date = models.DateField(db_column='HireDate', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'adminstaff'
    
    def __str__(self):
        return self.user.name

class Carts(models.Model):
    cart_id = models.AutoField(db_column='CartID', primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='UserID')
    created_at = models.DateTimeField(db_column='CreatedAt', auto_now_add=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'carts'

    def __str__(self):
        return f"Cart for {self.user.name}"

class Cartitems(models.Model):
    cart_item_id = models.AutoField(db_column='CartItemID', primary_key=True)
    cart = models.ForeignKey(Carts, on_delete=models.CASCADE, db_column='CartID')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, db_column='ProductID')
    quantity = models.IntegerField(db_column='Quantity', default=1)

    class Meta:
        managed = False
        db_table = 'cartitems'

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class Orders(models.Model):
    order_id = models.AutoField(db_column='OrderID', primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='UserID')
    order_date = models.DateTimeField(db_column='OrderDate', auto_now_add=True, blank=True, null=True)
    total_amount = models.DecimalField(db_column='TotalAmount', max_digits=12, decimal_places=2)
    status = models.CharField(db_column='Status', max_length=10, blank=True, null=True)
    shipping_address = models.TextField(db_column='ShippingAddress', blank=True, null=True)
    shipping_tracking_no = models.CharField(db_column='ShippingTrackingNo', max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders'
    
    def __str__(self):
        return f"Order #{self.order_id} by {self.user.name}"

class Orderitems(models.Model):
    order_item_id = models.AutoField(db_column='OrderItemID', primary_key=True)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, db_column='OrderID')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, db_column='ProductID')
    quantity = models.IntegerField(db_column='Quantity')
    price_at_purchase = models.DecimalField(db_column='PriceAtPurchase', max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'orderitems'
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.order_id}"

class Payments(models.Model):
    payment_id = models.AutoField(db_column='PaymentID', primary_key=True)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, db_column='OrderID')
    amount = models.DecimalField(db_column='Amount', max_digits=12, decimal_places=2)
    payment_date = models.DateTimeField(db_column='PaymentDate', auto_now_add=True, blank=True, null=True)
    payment_method = models.CharField(db_column='PaymentMethod', max_length=50, blank=True, null=True)
    transaction_id = models.CharField(db_column='TransactionID', max_length=200, blank=True, null=True)
    status = models.CharField(db_column='Status', max_length=9, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'payments'

    def __str__(self):
        return f"Payment {self.payment_id} for Order #{self.order.order_id}"

class Productfeedback(models.Model):
    feedback_id = models.AutoField(db_column='FeedbackID', primary_key=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, db_column='ProductID')
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='UserID')
    rating = models.IntegerField(db_column='Rating')
    comment = models.TextField(db_column='Comment', blank=True, null=True)
    submission_date = models.DateTimeField(db_column='SubmissionDate', auto_now_add=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'productfeedback'

    def __str__(self):
        return f"Feedback by {self.user.name} for {self.product.name}"

class Productlens(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, db_column='ProductID')
    lens_type = models.ForeignKey(Lenstypes, on_delete=models.CASCADE, db_column='LensTypeID')
    additional_cost = models.DecimalField(db_column='AdditionalCost', max_digits=8, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'productlens'

    def __str__(self):
        return f"{self.product.name} - {self.lens_type.name}"

# Models for other features
class Customframeorders(models.Model):
    custom_order_id = models.AutoField(db_column='CustomOrderID', primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='UserID')
    quantity = models.IntegerField(db_column='Quantity')
    shape = models.CharField(db_column='Shape', max_length=100, blank=True, null=True)
    color = models.CharField(db_column='Color', max_length=100, blank=True, null=True)
    material = models.CharField(db_column='Material', max_length=100, blank=True, null=True)
    logo_details = models.TextField(db_column='LogoDetails', blank=True, null=True)
    status = models.CharField(db_column='Status', max_length=12, blank=True, null=True)
    submission_date = models.DateTimeField(db_column='SubmissionDate', auto_now_add=True, blank=True, null=True)
    review_comments = models.TextField(db_column='ReviewComments', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customframeorders'
    
    def __str__(self):
        return f"Custom Order by {self.user.name}"

class Homeservicebookings(models.Model):
    booking_id = models.AutoField(db_column='BookingID', primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='UserID')
    service_type = models.CharField(db_column='ServiceType', max_length=100, blank=True, null=True)
    booking_date_time = models.DateTimeField(db_column='BookingDateTime', blank=True, null=True)
    address = models.TextField(db_column='Address', blank=True, null=True)
    status = models.CharField(db_column='Status', max_length=9, blank=True, null=True)
    assigned_staff = models.ForeignKey(Adminstaff, on_delete=models.SET_NULL, db_column='AssignedStaffID', blank=True, null=True)
    notes = models.TextField(db_column='Notes', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'homeservicebookings'

    def __str__(self):
        return f"Home Service for {self.user.name} on {self.booking_date_time}"

class Notifications(models.Model):
    notification_id = models.AutoField(db_column='NotificationID', primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='UserID')
    message = models.TextField(db_column='Message', blank=True, null=True)
    type = models.CharField(db_column='Type', max_length=50, blank=True, null=True)
    is_read = models.BooleanField(db_column='IsRead', default=False)
    creation_date = models.DateTimeField(db_column='CreationDate', auto_now_add=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notifications'

    def __str__(self):
        return f"Notification for {self.user.name}"

class Passwordresettokens(models.Model):
    token_id = models.AutoField(db_column='TokenID', primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='UserID')
    token = models.CharField(db_column='Token', max_length=255)
    expires_at = models.DateTimeField(db_column='ExpiresAt')
    used = models.BooleanField(db_column='Used', default=False)

    class Meta:
        managed = False
        db_table = 'passwordresettokens'

    def __str__(self):
        return f"Token for {self.user.name}"