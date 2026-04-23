# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
import os


class Address(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    fullname = models.CharField(max_length=100, db_column='fullName')  # Field name made lowercase.
    company = models.CharField(max_length=100)
    streetline1 = models.CharField(max_length=500, db_column='streetLine1')  # Field name made lowercase.
    streetline2 = models.CharField(db_column='streetLine2')  # Field name made lowercase.
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    postalcode = models.CharField(max_length=10, db_column='postalCode')  # Field name made lowercase.
    phonenumber = models.CharField(max_length=15, db_column='phoneNumber')  # Field name made lowercase.
    defaultshippingaddress = models.BooleanField(db_column='defaultShippingAddress')  # Field name made lowercase.
    defaultbillingaddress = models.BooleanField(db_column='defaultBillingAddress')  # Field name made lowercase.
    customerid = models.ForeignKey('Customer', on_delete=models.CASCADE, db_column='customerId', blank=True, null=True)  # Field name made lowercase.
    countryid = models.ForeignKey('Region', on_delete=models.CASCADE, db_column='countryId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'address'


class Administrator(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    deletedat = models.DateTimeField(db_column='deletedAt', blank=True, null=True)  # Field name made lowercase.
    firstname = models.CharField(db_column='firstName')  # Field name made lowercase.
    lastname = models.CharField(db_column='lastName')  # Field name made lowercase.
    emailaddress = models.CharField(db_column='emailAddress', unique=True)  # Field name made lowercase.
    userid = models.OneToOneField('User', on_delete=models.CASCADE, db_column='userId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'administrator'


class Asset(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(null=True, blank=True)
    mimetype = models.CharField(db_column='mimeType', null=True, blank=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    filesize = models.IntegerField(db_column='fileSize', blank=True, null=True)
    source = models.CharField(null=True, blank=True)
    preview = models.CharField(null=True, blank=True)
    focalpoint = models.TextField(db_column='focalPoint', blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

    def clean(self):
        if self.name:
            valid_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.svg']
            ext = os.path.splitext(self.name)[1].lower()
            if ext not in valid_extensions:
                raise ValidationError(f'Unsupported file extension: {ext}. Allowed: {", ".join(valid_extensions)}')

    class Meta:
        managed = False
        db_table = 'asset'


class AssetChannelsChannel(models.Model):
    assetid = models.OneToOneField('Asset', on_delete=models.CASCADE, db_column='assetId', primary_key=True)  # Field name made lowercase.
    channelid = models.ForeignKey('Channel', on_delete=models.CASCADE, db_column='channelId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'asset_channels_channel'
        unique_together = (('assetid', 'channelid'),)


class AssetTagsTag(models.Model):
    assetid = models.OneToOneField('Asset', on_delete=models.CASCADE, db_column='assetId', primary_key=True)  # Field name made lowercase.
    tagid = models.ForeignKey('Tag', on_delete=models.CASCADE, db_column='tagId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'asset_tags_tag'
        unique_together = (('assetid', 'tagid'),)


class AuthenticationMethod(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    identifier = models.CharField(blank=True, null=True)
    passwordhash = models.CharField(db_column='passwordHash', blank=True, null=True)  # Field name made lowercase.
    verificationtoken = models.CharField(db_column='verificationToken', blank=True, null=True)  # Field name made lowercase.
    passwordresettoken = models.CharField(db_column='passwordResetToken', blank=True, null=True)  # Field name made lowercase.
    identifierchangetoken = models.CharField(db_column='identifierChangeToken', blank=True, null=True)  # Field name made lowercase.
    pendingidentifier = models.CharField(db_column='pendingIdentifier', blank=True, null=True)  # Field name made lowercase.
    strategy = models.CharField(blank=True, null=True)
    externalidentifier = models.CharField(db_column='externalIdentifier', blank=True, null=True)  # Field name made lowercase.
    metadata = models.TextField(blank=True, null=True)
    type = models.CharField()
    userid = models.ForeignKey('User', on_delete=models.CASCADE, db_column='userId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'authentication_method'


class Channel(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    code = models.CharField(unique=True)
    token = models.CharField(unique=True)
    description = models.CharField(blank=True, null=True)
    defaultlanguagecode = models.CharField(db_column='defaultLanguageCode')  # Field name made lowercase.
    availablelanguagecodes = models.TextField(db_column='availableLanguageCodes', blank=True, null=True)  # Field name made lowercase.
    defaultcurrencycode = models.CharField(db_column='defaultCurrencyCode')  # Field name made lowercase.
    availablecurrencycodes = models.TextField(db_column='availableCurrencyCodes', blank=True, null=True)  # Field name made lowercase.
    trackinventory = models.BooleanField(db_column='trackInventory')  # Field name made lowercase.
    outofstockthreshold = models.IntegerField(db_column='outOfStockThreshold')  # Field name made lowercase.
    pricesincludetax = models.BooleanField(db_column='pricesIncludeTax')  # Field name made lowercase.
    sellerid = models.ForeignKey('Seller', on_delete=models.CASCADE, db_column='sellerId', blank=True, null=True)  # Field name made lowercase.
    defaulttaxzoneid = models.ForeignKey('Zone', on_delete=models.CASCADE, db_column='defaultTaxZoneId', blank=True, null=True)  # Field name made lowercase.
    defaultshippingzoneid = models.ForeignKey('Zone', on_delete=models.CASCADE, db_column='defaultShippingZoneId', related_name='channel_defaultshippingzoneid_set', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'channel'


class Collection(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    isroot = models.BooleanField(db_column='isRoot')  # Field name made lowercase.
    position = models.IntegerField()
    isprivate = models.BooleanField(db_column='isPrivate')  # Field name made lowercase.
    filters = models.TextField()
    inheritfilters = models.BooleanField(db_column='inheritFilters')  # Field name made lowercase.
    parentid = models.ForeignKey('Collection', on_delete=models.CASCADE, db_column='parentId', blank=True, null=True)  # Field name made lowercase.
    featuredassetid = models.ForeignKey('Asset', on_delete=models.CASCADE, db_column='featuredAssetId', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.name

    @property
    def name(self):
        """Property to get the English name of the collection"""
        trans = self.collectiontranslation_set.filter(languagecode='en').first()
        return trans.name if trans else f"Collection #{self.id}"

    def get_translation(self, language_code='en'):
        """Get collection translation for specific language"""
        try:
            return self.collectiontranslation_set.get(languagecode=language_code)
        except CollectionTranslation.DoesNotExist:
            return None
    
    def get_name(self, language_code='en'):
        """Get category name in specific language"""
        translation = self.get_translation(language_code)
        return translation.name if translation else f"Category {self.id}"
    
    class Meta:
        managed = False
        db_table = 'collection'


class CollectionAsset(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    assetid = models.ForeignKey('Asset', on_delete=models.CASCADE, db_column='assetId')  # Field name made lowercase.
    position = models.IntegerField()
    collectionid = models.ForeignKey('Collection', on_delete=models.CASCADE, db_column='collectionId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'collection_asset'


class CollectionChannelsChannel(models.Model):
    collectionid = models.OneToOneField('Collection', on_delete=models.CASCADE, db_column='collectionId', primary_key=True)  # Field name made lowercase.
    channelid = models.ForeignKey('Channel', on_delete=models.CASCADE, db_column='channelId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'collection_channels_channel'
        unique_together = (('collectionid', 'channelid'),)


class CollectionClosure(models.Model):
    """Vendure closure table: (ancestor, descendant) pairs; composite PK in DB."""
    pk = models.CompositePrimaryKey("id_ancestor", "id_descendant")
    id_ancestor = models.ForeignKey(
        "Collection",
        on_delete=models.CASCADE,
        db_column="id_ancestor",
        related_name="closure_as_ancestor",
    )
    id_descendant = models.ForeignKey(
        "Collection",
        on_delete=models.CASCADE,
        db_column="id_descendant",
        related_name="closure_as_descendant",
    )

    class Meta:
        managed = False
        db_table = "collection_closure"


class CollectionProductVariantsProductVariant(models.Model):
    """Join table: many variants per collection (Vendure M2M)."""
    pk = models.CompositePrimaryKey("collectionid", "productvariantid")
    collectionid = models.ForeignKey(
        "Collection",
        on_delete=models.CASCADE,
        db_column="collectionId",
    )
    productvariantid = models.ForeignKey(
        "ProductVariant",
        on_delete=models.CASCADE,
        db_column="productVariantId",
    )

    class Meta:
        managed = False
        db_table = "collection_product_variants_product_variant"


class CollectionTranslation(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    languagecode = models.CharField(db_column='languageCode', default='en')
    name = models.CharField()
    slug = models.CharField(blank=True)
    description = models.TextField()
    baseid = models.ForeignKey('Collection', on_delete=models.CASCADE, db_column='baseId', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.languagecode})"

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'collection_translation'


class Customer(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    deletedat = models.DateTimeField(db_column='deletedAt', blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(blank=True, null=True)
    firstname = models.CharField(db_column='firstName')  # Field name made lowercase.
    lastname = models.CharField(db_column='lastName')  # Field name made lowercase.
    phonenumber = models.CharField(db_column='phoneNumber', blank=True, null=True)  # Field name made lowercase.
    emailaddress = models.CharField(db_column='emailAddress')  # Field name made lowercase.
    userid = models.OneToOneField('User', on_delete=models.CASCADE, db_column='userId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'customer'


class CustomerChannelsChannel(models.Model):
    customerid = models.OneToOneField('Customer', on_delete=models.CASCADE, db_column='customerId', primary_key=True)  # Field name made lowercase.
    channelid = models.ForeignKey('Channel', on_delete=models.CASCADE, db_column='channelId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'customer_channels_channel'
        unique_together = (('customerid', 'channelid'),)


class CustomerGroup(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    name = models.CharField()

    class Meta:
        managed = False
        db_table = 'customer_group'


class CustomerGroupsCustomerGroup(models.Model):
    customerid = models.OneToOneField('Customer', on_delete=models.CASCADE, db_column='customerId', primary_key=True)  # Field name made lowercase.
    customergroupid = models.ForeignKey('CustomerGroup', on_delete=models.CASCADE, db_column='customerGroupId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'customer_groups_customer_group'
        unique_together = (('customerid', 'customergroupid'),)


class Facet(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    isprivate = models.BooleanField(db_column='isPrivate')  # Field name made lowercase.
    code = models.CharField(unique=True)

    class Meta:
        managed = False
        db_table = 'facet'


class FacetChannelsChannel(models.Model):
    facetid = models.OneToOneField('Facet', on_delete=models.CASCADE, db_column='facetId', primary_key=True)  # Field name made lowercase.
    channelid = models.ForeignKey('Channel', on_delete=models.CASCADE, db_column='channelId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'facet_channels_channel'
        unique_together = (('facetid', 'channelid'),)


class FacetTranslation(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    languagecode = models.CharField(db_column='languageCode')  # Field name made lowercase.
    name = models.CharField()
    baseid = models.ForeignKey('Facet', on_delete=models.CASCADE, db_column='baseId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'facet_translation'


class FacetValue(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    code = models.CharField()
    facetid = models.ForeignKey('Facet', on_delete=models.CASCADE, db_column='facetId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'facet_value'


class FacetValueChannelsChannel(models.Model):
    facetvalueid = models.OneToOneField('FacetValue', on_delete=models.CASCADE, db_column='facetValueId', primary_key=True)  # Field name made lowercase.
    channelid = models.ForeignKey('Channel', on_delete=models.CASCADE, db_column='channelId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'facet_value_channels_channel'
        unique_together = (('facetvalueid', 'channelid'),)


class FacetValueTranslation(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    languagecode = models.CharField(db_column='languageCode')  # Field name made lowercase.
    name = models.CharField()
    baseid = models.ForeignKey('FacetValue', on_delete=models.CASCADE, db_column='baseId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'facet_value_translation'


class Fulfillment(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    state = models.CharField()
    trackingcode = models.CharField(db_column='trackingCode')  # Field name made lowercase.
    method = models.CharField()
    handlercode = models.CharField(db_column='handlerCode')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'fulfillment'


class GlobalSettings(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    availablelanguages = models.TextField(db_column='availableLanguages')  # Field name made lowercase.
    trackinventory = models.BooleanField(db_column='trackInventory')  # Field name made lowercase.
    outofstockthreshold = models.IntegerField(db_column='outOfStockThreshold')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'global_settings'


class HistoryEntry(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    type = models.CharField()
    ispublic = models.BooleanField(db_column='isPublic')  # Field name made lowercase.
    data = models.TextField()
    discriminator = models.CharField()
    administratorid = models.ForeignKey('Administrator', on_delete=models.CASCADE, db_column='administratorId', blank=True, null=True)  # Field name made lowercase.
    customerid = models.ForeignKey('Customer', on_delete=models.CASCADE, db_column='customerId', blank=True, null=True)  # Field name made lowercase.
    orderid = models.ForeignKey('Order', on_delete=models.CASCADE, db_column='orderId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'history_entry'


class JobRecord(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    queuename = models.CharField(db_column='queueName')  # Field name made lowercase.
    data = models.TextField(blank=True, null=True)
    state = models.CharField()
    progress = models.IntegerField()
    result = models.TextField(blank=True, null=True)
    error = models.CharField(blank=True, null=True)
    startedat = models.DateTimeField(db_column='startedAt', blank=True, null=True)  # Field name made lowercase.
    settledat = models.DateTimeField(db_column='settledAt', blank=True, null=True)  # Field name made lowercase.
    issettled = models.BooleanField(db_column='isSettled')  # Field name made lowercase.
    retries = models.IntegerField()
    attempts = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'job_record'


class JobRecordBuffer(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    bufferid = models.CharField(db_column='bufferId')  # Field name made lowercase.
    job = models.TextField()

    class Meta:
        managed = False
        db_table = 'job_record_buffer'


class Migrations(models.Model):
    timestamp = models.BigIntegerField()
    name = models.CharField()

    class Meta:
        managed = False
        db_table = 'migrations'


class Order(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    type = models.CharField()
    code = models.CharField(unique=True)
    state = models.CharField()
    active = models.BooleanField()
    orderplacedat = models.DateTimeField(db_column='orderPlacedAt', blank=True, null=True)  # Field name made lowercase.
    couponcodes = models.TextField(db_column='couponCodes')  # Field name made lowercase.
    shippingaddress = models.TextField(db_column='shippingAddress')  # Field name made lowercase.
    billingaddress = models.TextField(db_column='billingAddress')  # Field name made lowercase.
    currencycode = models.CharField(db_column='currencyCode')  # Field name made lowercase.
    aggregateorderid = models.ForeignKey('Order', on_delete=models.CASCADE, db_column='aggregateOrderId', blank=True, null=True)  # Field name made lowercase.
    customerid = models.ForeignKey('Customer', on_delete=models.CASCADE, db_column='customerId', blank=True, null=True)  # Field name made lowercase.
    taxzoneid = models.IntegerField(db_column='taxZoneId', blank=True, null=True)  # Field name made lowercase.
    subtotal = models.IntegerField(db_column='subTotal')  # Field name made lowercase.
    subtotalwithtax = models.IntegerField(db_column='subTotalWithTax')  # Field name made lowercase.
    shipping = models.IntegerField()
    shippingwithtax = models.IntegerField(db_column='shippingWithTax')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'order'


class OrderChannelsChannel(models.Model):
    orderid = models.OneToOneField('Order', on_delete=models.CASCADE, db_column='orderId', primary_key=True)  # Field name made lowercase.
    channelid = models.ForeignKey('Channel', on_delete=models.CASCADE, db_column='channelId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'order_channels_channel'
        unique_together = (('orderid', 'channelid'),)


class OrderFulfillmentsFulfillment(models.Model):
    orderid = models.OneToOneField('Order', on_delete=models.CASCADE, db_column='orderId', primary_key=True)  # Field name made lowercase.
    fulfillmentid = models.ForeignKey('Fulfillment', on_delete=models.CASCADE, db_column='fulfillmentId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'order_fulfillments_fulfillment'
        unique_together = (('orderid', 'fulfillmentid'),)


class OrderLine(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    quantity = models.IntegerField()
    orderplacedquantity = models.IntegerField(db_column='orderPlacedQuantity')  # Field name made lowercase.
    listpriceincludestax = models.BooleanField(db_column='listPriceIncludesTax')  # Field name made lowercase.
    adjustments = models.TextField()
    taxlines = models.TextField(db_column='taxLines')  # Field name made lowercase.
    sellerchannelid = models.ForeignKey('Seller', on_delete=models.CASCADE, db_column='sellerChannelId', blank=True, null=True)  # Field name made lowercase.
    shippinglineid = models.ForeignKey('ShippingLine', on_delete=models.CASCADE, db_column='shippingLineId', blank=True, null=True)  # Field name made lowercase.
    productvariantid = models.ForeignKey('ProductVariant', on_delete=models.CASCADE, db_column='productVariantId')  # Field name made lowercase.
    taxcategoryid = models.ForeignKey('TaxCategory', on_delete=models.CASCADE, db_column='taxCategoryId', blank=True, null=True)  # Field name made lowercase.
    initiallistprice = models.IntegerField(db_column='initialListPrice', blank=True, null=True)  # Field name made lowercase.
    listprice = models.IntegerField(db_column='listPrice')  # Field name made lowercase.
    featuredassetid = models.ForeignKey('Asset', on_delete=models.CASCADE, db_column='featuredAssetId', blank=True, null=True)  # Field name made lowercase.
    orderid = models.ForeignKey('Order', on_delete=models.CASCADE, db_column='orderId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'order_line'


class OrderLineReference(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    quantity = models.IntegerField()
    fulfillmentid = models.ForeignKey('Fulfillment', on_delete=models.CASCADE, db_column='fulfillmentId', blank=True, null=True)  # Field name made lowercase.
    modificationid = models.ForeignKey('OrderModification', on_delete=models.CASCADE, db_column='modificationId', blank=True, null=True)  # Field name made lowercase.
    orderlineid = models.ForeignKey('OrderLine', on_delete=models.CASCADE, db_column='orderLineId')  # Field name made lowercase.
    refundid = models.ForeignKey('Refund', on_delete=models.CASCADE, db_column='refundId', blank=True, null=True)  # Field name made lowercase.
    discriminator = models.CharField()

    class Meta:
        managed = False
        db_table = 'order_line_reference'


class OrderModification(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    note = models.CharField()
    shippingaddresschange = models.TextField(db_column='shippingAddressChange', blank=True, null=True)  # Field name made lowercase.
    billingaddresschange = models.TextField(db_column='billingAddressChange', blank=True, null=True)  # Field name made lowercase.
    pricechange = models.IntegerField(db_column='priceChange')  # Field name made lowercase.
    orderid = models.ForeignKey('Order', on_delete=models.CASCADE, db_column='orderId', blank=True, null=True)  # Field name made lowercase.
    paymentid = models.ForeignKey('Payment', on_delete=models.CASCADE, db_column='paymentId', blank=True, null=True)  # Field name made lowercase.
    refundid = models.ForeignKey('Refund', on_delete=models.CASCADE, db_column='refundId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'order_modification'


class OrderPromotionsPromotion(models.Model):
    orderid = models.OneToOneField('Order', on_delete=models.CASCADE, db_column='orderId', primary_key=True)  # Field name made lowercase.
    promotionid = models.ForeignKey('Promotion', on_delete=models.CASCADE, db_column='promotionId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'order_promotions_promotion'
        unique_together = (('orderid', 'promotionid'),)


class Payment(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    method = models.CharField()
    state = models.CharField()
    errormessage = models.CharField(db_column='errorMessage', blank=True, null=True)  # Field name made lowercase.
    transactionid = models.CharField(db_column='transactionId', blank=True, null=True)  # Field name made lowercase.
    metadata = models.TextField()
    amount = models.IntegerField()
    orderid = models.ForeignKey('Order', on_delete=models.CASCADE, db_column='orderId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'payment'


class PaymentMethod(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    code = models.CharField()
    enabled = models.BooleanField()
    checker = models.TextField(blank=True, null=True)
    handler = models.TextField()

    class Meta:
        managed = False
        db_table = 'payment_method'


class PaymentMethodChannelsChannel(models.Model):
    paymentmethodid = models.OneToOneField('PaymentMethod', on_delete=models.CASCADE, db_column='paymentMethodId', primary_key=True)  # Field name made lowercase.
    channelid = models.ForeignKey('Channel', on_delete=models.CASCADE, db_column='channelId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'payment_method_channels_channel'
        unique_together = (('paymentmethodid', 'channelid'),)


class PaymentMethodTranslation(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    languagecode = models.CharField(db_column='languageCode')  # Field name made lowercase.
    name = models.CharField()
    description = models.TextField()
    baseid = models.ForeignKey('PaymentMethod', on_delete=models.CASCADE, db_column='baseId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'payment_method_translation'


class Product(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    deletedat = models.DateTimeField(db_column='deletedAt', blank=True, null=True)
    enabled = models.BooleanField(default=True)
    featuredassetid = models.ForeignKey('Asset', on_delete=models.CASCADE, db_column='featuredAssetId', blank=True, null=True)

    def __str__(self):
        trans = self.producttranslation_set.filter(languagecode='en').first()
        return trans.name if trans else f"Product #{self.id}"

    class Meta:
        managed = False
        db_table = 'product'


class ProductAsset(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    assetid = models.ForeignKey('Asset', on_delete=models.CASCADE, db_column='assetId')
    position = models.IntegerField(null=True, blank=True)
    productid = models.ForeignKey('Product', on_delete=models.CASCADE, db_column='productId')

    class Meta:
        managed = False
        db_table = 'product_asset'


class ProductChannelsChannel(models.Model):
    productid = models.OneToOneField('Product', on_delete=models.CASCADE, db_column='productId', primary_key=True)  # Field name made lowercase.
    channelid = models.ForeignKey('Channel', on_delete=models.CASCADE, db_column='channelId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'product_channels_channel'
        unique_together = (('productid', 'channelid'),)


class ProductFacetValuesFacetValue(models.Model):
    productid = models.OneToOneField('Product', on_delete=models.CASCADE, db_column='productId', primary_key=True)  # Field name made lowercase.
    facetvalueid = models.ForeignKey('FacetValue', on_delete=models.CASCADE, db_column='facetValueId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'product_facet_values_facet_value'
        unique_together = (('productid', 'facetvalueid'),)


class ProductOption(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    deletedat = models.DateTimeField(db_column='deletedAt', blank=True, null=True)  # Field name made lowercase.
    code = models.CharField()
    groupid = models.ForeignKey('ProductOptionGroup', on_delete=models.CASCADE, db_column='groupId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'product_option'


class ProductOptionGroup(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    deletedat = models.DateTimeField(db_column='deletedAt', blank=True, null=True)  # Field name made lowercase.
    code = models.CharField()
    productid = models.ForeignKey('Product', on_delete=models.CASCADE, db_column='productId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'product_option_group'


class ProductOptionGroupTranslation(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    languagecode = models.CharField(db_column='languageCode')  # Field name made lowercase.
    name = models.CharField()
    baseid = models.ForeignKey('ProductOptionGroup', on_delete=models.CASCADE, db_column='baseId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'product_option_group_translation'


class ProductOptionTranslation(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    languagecode = models.CharField(db_column='languageCode')  # Field name made lowercase.
    name = models.CharField()
    baseid = models.ForeignKey('ProductOption', on_delete=models.CASCADE, db_column='baseId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'product_option_translation'


class ProductTranslation(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    languagecode = models.CharField(db_column='languageCode', default='en')
    name = models.CharField()
    slug = models.CharField(blank=True)
    description = models.TextField()
    baseid = models.ForeignKey('Product', on_delete=models.CASCADE, db_column='baseId', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'product_translation'


class ProductVariant(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    deletedat = models.DateTimeField(db_column='deletedAt', blank=True, null=True)
    enabled = models.BooleanField(default=True)
    sku = models.CharField()
    outofstockthreshold = models.IntegerField(db_column='outOfStockThreshold', default=0)
    useglobaloutofstockthreshold = models.BooleanField(db_column='useGlobalOutOfStockThreshold', default=True)
    trackinventory = models.CharField(db_column='trackInventory', default='INHERIT')
    featuredassetid = models.ForeignKey('Asset', on_delete=models.CASCADE, db_column='featuredAssetId', blank=True, null=True)
    taxcategoryid = models.ForeignKey('TaxCategory', on_delete=models.CASCADE, db_column='taxCategoryId', blank=True, null=True)
    productid = models.ForeignKey('Product', on_delete=models.CASCADE, db_column='productId', blank=True, null=True)

    def __str__(self):
        return f"{self.sku}"

    def get_translation(self, language_code='en'):
        """Get product variant translation"""
        try:
            return self.productvarianttranslation_set.get(languagecode=language_code)
        except Exception:
            return None
    
    def get_name(self, language_code='en'):
        """Get product name"""
        translation = self.get_translation(language_code)
        if translation and translation.name:
            return translation.name
        return f"Variant {self.sku}"
    
    def get_product_name(self, language_code='en'):
        """Get parent product name"""
        if self.productid:
            translation = self.productid.producttranslation_set.filter(languagecode=language_code).first()
            if translation:
                return translation.name
        return self.get_name(language_code)
    
    def get_price(self):
        """Get price (adjust based on your price model)"""
        price = self.productvariantprice_set.filter(channelid__isnull=True).first()
        return price.price if price else 0
    
    class Meta:
        managed = False
        db_table = 'product_variant'


class ProductVariantAsset(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    assetid = models.ForeignKey('Asset', on_delete=models.CASCADE, db_column='assetId')  # Field name made lowercase.
    position = models.IntegerField()
    productvariantid = models.ForeignKey('ProductVariant', on_delete=models.CASCADE, db_column='productVariantId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'product_variant_asset'


class ProductVariantChannelsChannel(models.Model):
    productvariantid = models.OneToOneField('ProductVariant', on_delete=models.CASCADE, db_column='productVariantId', primary_key=True)  # Field name made lowercase.
    channelid = models.ForeignKey('Channel', on_delete=models.CASCADE, db_column='channelId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'product_variant_channels_channel'
        unique_together = (('productvariantid', 'channelid'),)


class ProductVariantFacetValuesFacetValue(models.Model):
    productvariantid = models.OneToOneField('ProductVariant', on_delete=models.CASCADE, db_column='productVariantId', primary_key=True)  # Field name made lowercase.
    facetvalueid = models.ForeignKey('FacetValue', on_delete=models.CASCADE, db_column='facetValueId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'product_variant_facet_values_facet_value'
        unique_together = (('productvariantid', 'facetvalueid'),)


class ProductVariantOptionsProductOption(models.Model):
    productvariantid = models.OneToOneField('ProductVariant', on_delete=models.CASCADE, db_column='productVariantId', primary_key=True)  # Field name made lowercase.
    productoptionid = models.ForeignKey('ProductOption', on_delete=models.CASCADE, db_column='productOptionId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'product_variant_options_product_option'
        unique_together = (('productvariantid', 'productoptionid'),)


class ProductVariantPrice(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    currencycode = models.CharField(db_column='currencyCode', default='PKR')
    channelid = models.IntegerField(db_column='channelId', blank=True, null=True)
    price = models.IntegerField()
    variantid = models.ForeignKey('ProductVariant', on_delete=models.CASCADE, db_column='variantId', blank=True, null=True)

    def __str__(self):
        return f"{self.price} {self.currencycode}"

    class Meta:
        managed = False
        db_table = 'product_variant_price'


class ProductVariantTranslation(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    languagecode = models.CharField(db_column='languageCode', default='en')
    name = models.CharField()
    baseid = models.ForeignKey('ProductVariant', on_delete=models.CASCADE, db_column='baseId', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'product_variant_translation'

# Signals for automation
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=ProductTranslation)
def sync_variant_translation(sender, instance, created, **kwargs):
    """Automatically update variant translations when product translation is saved"""
    if instance.baseid:
        variants = ProductVariant.objects.filter(productid=instance.baseid)
        for variant in variants:
            ProductVariantTranslation.objects.update_or_create(
                baseid=variant,
                languagecode=instance.languagecode,
                defaults={'name': instance.name}
            )


class Promotion(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    deletedat = models.DateTimeField(db_column='deletedAt', blank=True, null=True)  # Field name made lowercase.
    startsat = models.DateTimeField(db_column='startsAt', blank=True, null=True)  # Field name made lowercase.
    endsat = models.DateTimeField(db_column='endsAt', blank=True, null=True)  # Field name made lowercase.
    couponcode = models.CharField(db_column='couponCode', blank=True, null=True)  # Field name made lowercase.
    percustomerusagelimit = models.IntegerField(db_column='perCustomerUsageLimit', blank=True, null=True)  # Field name made lowercase.
    usagelimit = models.IntegerField(db_column='usageLimit', blank=True, null=True)  # Field name made lowercase.
    enabled = models.BooleanField()
    conditions = models.TextField()
    actions = models.TextField()
    priorityscore = models.IntegerField(db_column='priorityScore')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'promotion'


class PromotionChannelsChannel(models.Model):
    promotionid = models.OneToOneField('Promotion', on_delete=models.CASCADE, db_column='promotionId', primary_key=True)  # Field name made lowercase.
    channelid = models.ForeignKey('Channel', on_delete=models.CASCADE, db_column='channelId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'promotion_channels_channel'
        unique_together = (('promotionid', 'channelid'),)


class PromotionTranslation(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    languagecode = models.CharField(db_column='languageCode')  # Field name made lowercase.
    name = models.CharField()
    description = models.TextField()
    baseid = models.ForeignKey('Promotion', on_delete=models.CASCADE, db_column='baseId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'promotion_translation'


class Refund(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    method = models.CharField()
    reason = models.CharField(blank=True, null=True)
    state = models.CharField()
    transactionid = models.CharField(db_column='transactionId', blank=True, null=True)  # Field name made lowercase.
    metadata = models.TextField()
    paymentid = models.ForeignKey('Payment', on_delete=models.CASCADE, db_column='paymentId')  # Field name made lowercase.
    items = models.IntegerField()
    shipping = models.IntegerField()
    adjustment = models.IntegerField()
    total = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'refund'


class Region(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    code = models.CharField()
    type = models.CharField()
    enabled = models.BooleanField()
    parentid = models.ForeignKey('self', on_delete=models.CASCADE, db_column='parentId', blank=True, null=True)  # Field name made lowercase.
    discriminator = models.CharField()

    class Meta:
        managed = False
        db_table = 'region'


class RegionTranslation(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    languagecode = models.CharField(db_column='languageCode')  # Field name made lowercase.
    name = models.CharField()
    baseid = models.ForeignKey('Region', on_delete=models.CASCADE, db_column='baseId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'region_translation'


class Role(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    code = models.CharField()
    description = models.CharField()
    permissions = models.TextField()

    class Meta:
        managed = False
        db_table = 'role'


class RoleChannelsChannel(models.Model):
    roleid = models.OneToOneField('Role', on_delete=models.CASCADE, db_column='roleId', primary_key=True)  # Field name made lowercase.
    channelid = models.ForeignKey('Channel', on_delete=models.CASCADE, db_column='channelId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'role_channels_channel'
        unique_together = (('roleid', 'channelid'),)


class ScheduledTaskRecord(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    taskid = models.CharField(db_column='taskId', unique=True)  # Field name made lowercase.
    enabled = models.BooleanField()
    lockedat = models.DateTimeField(db_column='lockedAt', blank=True, null=True)  # Field name made lowercase.
    lastexecutedat = models.DateTimeField(db_column='lastExecutedAt', blank=True, null=True)  # Field name made lowercase.
    manuallytriggeredat = models.DateTimeField(db_column='manuallyTriggeredAt', blank=True, null=True)  # Field name made lowercase.
    lastresult = models.TextField(db_column='lastResult', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'scheduled_task_record'


class SearchIndexItem(models.Model):
    languagecode = models.CharField(db_column='languageCode', primary_key=True)  # Field name made lowercase.
    enabled = models.BooleanField()
    productname = models.CharField(db_column='productName')  # Field name made lowercase.
    productvariantname = models.CharField(db_column='productVariantName')  # Field name made lowercase.
    description = models.TextField()
    slug = models.CharField()
    sku = models.CharField()
    facetids = models.TextField(db_column='facetIds')  # Field name made lowercase.
    facetvalueids = models.TextField(db_column='facetValueIds')  # Field name made lowercase.
    collectionids = models.TextField(db_column='collectionIds')  # Field name made lowercase.
    collectionslugs = models.TextField(db_column='collectionSlugs')  # Field name made lowercase.
    channelids = models.TextField(db_column='channelIds')  # Field name made lowercase.
    productpreview = models.CharField(db_column='productPreview')  # Field name made lowercase.
    productpreviewfocalpoint = models.TextField(db_column='productPreviewFocalPoint', blank=True, null=True)  # Field name made lowercase.
    productvariantpreview = models.CharField(db_column='productVariantPreview')  # Field name made lowercase.
    productvariantpreviewfocalpoint = models.TextField(db_column='productVariantPreviewFocalPoint', blank=True, null=True)  # Field name made lowercase.
    instock = models.BooleanField(db_column='inStock')  # Field name made lowercase.
    productinstock = models.BooleanField(db_column='productInStock')  # Field name made lowercase.
    productvariantid = models.IntegerField(db_column='productVariantId')  # Field name made lowercase.
    channelid = models.IntegerField(db_column='channelId')  # Field name made lowercase.
    productid = models.IntegerField(db_column='productId')  # Field name made lowercase.
    productassetid = models.IntegerField(db_column='productAssetId', blank=True, null=True)  # Field name made lowercase.
    productvariantassetid = models.IntegerField(db_column='productVariantAssetId', blank=True, null=True)  # Field name made lowercase.
    price = models.IntegerField()
    pricewithtax = models.IntegerField(db_column='priceWithTax')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'search_index_item'
        unique_together = (('languagecode', 'productvariantid', 'channelid'),)


class Seller(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    deletedat = models.DateTimeField(db_column='deletedAt', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField()

    class Meta:
        managed = False
        db_table = 'seller'


class Session(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    token = models.CharField(unique=True)
    expires = models.DateTimeField()
    invalidated = models.BooleanField()
    authenticationstrategy = models.CharField(db_column='authenticationStrategy', blank=True, null=True)  # Field name made lowercase.
    activeorderid = models.ForeignKey('Order', on_delete=models.CASCADE, db_column='activeOrderId', blank=True, null=True)  # Field name made lowercase.
    activechannelid = models.ForeignKey('Channel', on_delete=models.CASCADE, db_column='activeChannelId', blank=True, null=True)  # Field name made lowercase.
    type = models.CharField()
    userid = models.ForeignKey('User', on_delete=models.CASCADE, db_column='userId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'session'


class SettingsStoreEntry(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    key = models.CharField()
    value = models.TextField(blank=True, null=True)  # This field type is a guess.
    scope = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'settings_store_entry'
        unique_together = (('key', 'scope'),)


class ShippingLine(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    listpriceincludestax = models.BooleanField(db_column='listPriceIncludesTax')  # Field name made lowercase.
    adjustments = models.TextField()
    taxlines = models.TextField(db_column='taxLines')  # Field name made lowercase.
    shippingmethodid = models.ForeignKey('ShippingMethod', on_delete=models.CASCADE, db_column='shippingMethodId')  # Field name made lowercase.
    listprice = models.IntegerField(db_column='listPrice')  # Field name made lowercase.
    orderid = models.ForeignKey('Order', on_delete=models.CASCADE, db_column='orderId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'shipping_line'


class ShippingMethod(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    deletedat = models.DateTimeField(db_column='deletedAt', blank=True, null=True)  # Field name made lowercase.
    code = models.CharField()
    checker = models.TextField()
    calculator = models.TextField()
    fulfillmenthandlercode = models.CharField(db_column='fulfillmentHandlerCode')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'shipping_method'


class ShippingMethodChannelsChannel(models.Model):
    shippingmethodid = models.OneToOneField('ShippingMethod', on_delete=models.CASCADE, db_column='shippingMethodId', primary_key=True)  # Field name made lowercase.
    channelid = models.ForeignKey('Channel', on_delete=models.CASCADE, db_column='channelId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'shipping_method_channels_channel'
        unique_together = (('shippingmethodid', 'channelid'),)


class ShippingMethodTranslation(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    languagecode = models.CharField(db_column='languageCode')  # Field name made lowercase.
    name = models.CharField()
    description = models.CharField()
    baseid = models.ForeignKey('ShippingMethod', on_delete=models.CASCADE, db_column='baseId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'shipping_method_translation'


class StockLevel(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    stockonhand = models.IntegerField(db_column='stockOnHand')  # Field name made lowercase.
    stockallocated = models.IntegerField(db_column='stockAllocated')  # Field name made lowercase.
    productvariantid = models.ForeignKey('ProductVariant', on_delete=models.CASCADE, db_column='productVariantId')  # Field name made lowercase.
    stocklocationid = models.ForeignKey('StockLocation', on_delete=models.CASCADE, db_column='stockLocationId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'stock_level'
        unique_together = (('productvariantid', 'stocklocationid'),)


class StockLocation(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    name = models.CharField()
    description = models.CharField()

    class Meta:
        managed = False
        db_table = 'stock_location'


class StockLocationChannelsChannel(models.Model):
    stocklocationid = models.OneToOneField('StockLocation', on_delete=models.CASCADE, db_column='stockLocationId', primary_key=True)  # Field name made lowercase.
    channelid = models.ForeignKey('Channel', on_delete=models.CASCADE, db_column='channelId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'stock_location_channels_channel'
        unique_together = (('stocklocationid', 'channelid'),)


class StockMovement(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    type = models.CharField()
    quantity = models.IntegerField()
    stocklocationid = models.ForeignKey('StockLocation', on_delete=models.CASCADE, db_column='stockLocationId')  # Field name made lowercase.
    discriminator = models.CharField()
    productvariantid = models.ForeignKey('ProductVariant', on_delete=models.CASCADE, db_column='productVariantId', blank=True, null=True)  # Field name made lowercase.
    orderlineid = models.ForeignKey('OrderLine', on_delete=models.CASCADE, db_column='orderLineId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'stock_movement'


class Surcharge(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    description = models.CharField()
    listpriceincludestax = models.BooleanField(db_column='listPriceIncludesTax')  # Field name made lowercase.
    sku = models.CharField()
    taxlines = models.TextField(db_column='taxLines')  # Field name made lowercase.
    listprice = models.IntegerField(db_column='listPrice')  # Field name made lowercase.
    orderid = models.ForeignKey('Order', on_delete=models.CASCADE, db_column='orderId', blank=True, null=True)  # Field name made lowercase.
    ordermodificationid = models.ForeignKey('OrderModification', on_delete=models.CASCADE, db_column='orderModificationId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'surcharge'


class Tag(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    value = models.CharField()

    class Meta:
        managed = False
        db_table = 'tag'


class TaxCategory(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    name = models.CharField()
    isdefault = models.BooleanField(db_column='isDefault')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tax_category'


class TaxRate(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    name = models.CharField()
    enabled = models.BooleanField()
    value = models.DecimalField(max_digits=5, decimal_places=2)
    categoryid = models.ForeignKey('TaxCategory', on_delete=models.CASCADE, db_column='categoryId', blank=True, null=True)  # Field name made lowercase.
    zoneid = models.ForeignKey('Zone', on_delete=models.CASCADE, db_column='zoneId', blank=True, null=True)  # Field name made lowercase.
    customergroupid = models.ForeignKey('CustomerGroup', on_delete=models.CASCADE, db_column='customerGroupId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tax_rate'


class User(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    deletedat = models.DateTimeField(db_column='deletedAt', blank=True, null=True)  # Field name made lowercase.
    identifier = models.CharField()
    verified = models.BooleanField()
    lastlogin = models.DateTimeField(db_column='lastLogin', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user'

class Zone(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    name = models.CharField()

    class Meta:
        managed = False
        db_table = 'zone'


class ZoneMembersRegion(models.Model):
    zoneid = models.OneToOneField('Zone', on_delete=models.CASCADE, db_column='zoneId', primary_key=True)  # Field name made lowercase.
    regionid = models.ForeignKey('Region', on_delete=models.CASCADE, db_column='regionId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'zone_members_region'
        unique_together = (('zoneid', 'regionid'),)

class UserRolesRole(models.Model):
    userid = models.OneToOneField('User', on_delete=models.CASCADE, db_column='userId', primary_key=True)  # Field name made lowercase.
    roleid = models.ForeignKey('Role', on_delete=models.CASCADE, db_column='roleId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user_roles_role'
        unique_together = (('userid', 'roleid'),)

class MerchantProfile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='merchant_profile')
    merchant_type = models.CharField(max_length=50, choices=[('individual', 'Individual'), ('business', 'Registered Business')])
    ntn = models.CharField(max_length=20, blank=True, null=True, verbose_name="NTN Number")
    cnic = models.CharField(max_length=15, blank=True, null=True, verbose_name="CNIC Number")
    utility_bill = models.FileField(upload_to='merchant_docs/bills/', blank=True, null=True)
    cnic_front = models.FileField(upload_to='merchant_docs/cnic/', blank=True, null=True)
    cnic_back = models.FileField(upload_to='merchant_docs/cnic/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Merchant: {self.user.identifier}"
