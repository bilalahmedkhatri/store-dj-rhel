from unfold.admin import ModelAdmin
from django.contrib import admin
from .models import (
    Address, Administrator, Asset, AssetChannelsChannel, AssetTagsTag,
    AuthenticationMethod, Channel, Collection, CollectionAsset,
    CollectionChannelsChannel, CollectionClosure, 
    CollectionProductVariantsProductVariant, CollectionTranslation,
    Customer, CustomerChannelsChannel, CustomerGroup,
    CustomerGroupsCustomerGroup, Facet, FacetChannelsChannel,
    FacetTranslation, FacetValue, FacetValueChannelsChannel,
    FacetValueTranslation, Fulfillment, GlobalSettings,
    HistoryEntry, JobRecord, JobRecordBuffer, Migrations,
    Order, OrderChannelsChannel, OrderFulfillmentsFulfillment,
    OrderLine, OrderLineReference, OrderModification,
    OrderPromotionsPromotion, Payment, PaymentMethod,
    PaymentMethodChannelsChannel, PaymentMethodTranslation,
    Product, ProductAsset, ProductChannelsChannel,
    ProductFacetValuesFacetValue, ProductOption, ProductOptionGroup,
    ProductOptionGroupTranslation, ProductOptionTranslation,
    ProductTranslation, ProductVariant, ProductVariantAsset,
    ProductVariantChannelsChannel, ProductVariantFacetValuesFacetValue,
    ProductVariantOptionsProductOption, ProductVariantPrice,
    ProductVariantTranslation, Promotion, PromotionChannelsChannel,
    PromotionTranslation, Refund, Region, RegionTranslation,
    Role, RoleChannelsChannel, ScheduledTaskRecord, SearchIndexItem,
    Seller, Session, SettingsStoreEntry, ShippingLine,
    ShippingMethod, ShippingMethodChannelsChannel,
    ShippingMethodTranslation, StockLevel, StockLocation,
    StockLocationChannelsChannel, StockMovement, Surcharge,
    Tag, TaxCategory, TaxRate, User, Zone,
    ZoneMembersRegion, UserRolesRole, MerchantProfile
)

# Admin Branding
admin.site.site_header = "e-sahulat Administration"
admin.site.site_title = "e-sahulat Admin Portal"
admin.site.index_title = "Welcome to e-sahulat Management Dashboard"

@admin.register(MerchantProfile)
class MerchantProfileAdmin(ModelAdmin):
    list_display = ('user', 'merchant_type', 'ntn', 'cnic', 'is_verified', 'created_at')
    list_filter = ('merchant_type', 'is_verified', 'created_at')
    search_fields = ('user__identifier', 'ntn', 'cnic')

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ('id', 'enabled', 'createdat', 'updatedat')
    list_filter = ('enabled', 'createdat')
    search_fields = ('id',)

@admin.register(ProductTranslation)
class ProductTranslationAdmin(ModelAdmin):
    list_display = ('name', 'slug', 'languagecode', 'baseid')
    list_filter = ('languagecode',)
    search_fields = ('name', 'slug')

@admin.register(ProductVariant)
class ProductVariantAdmin(ModelAdmin):
    list_display = ('sku', 'productid', 'enabled', 'trackinventory')
    list_filter = ('enabled', 'trackinventory')
    search_fields = ('sku',)

@admin.register(ProductVariantTranslation)
class ProductVariantTranslationAdmin(ModelAdmin):
    list_display = ('name', 'languagecode', 'baseid')
    list_filter = ('languagecode',)
    search_fields = ('name',)

@admin.register(ProductVariantPrice)
class ProductVariantPriceAdmin(ModelAdmin):
    list_display = ('variantid', 'price', 'currencycode')
    list_filter = ('currencycode',)
    search_fields = ('variantid__sku',)

@admin.register(Collection)
class CollectionAdmin(ModelAdmin):
    list_display = ('id', 'isroot', 'position', 'parentid')
    list_filter = ('isroot', 'isprivate')
    search_fields = ('id',)

@admin.register(CollectionTranslation)
class CollectionTranslationAdmin(ModelAdmin):
    list_display = ('name', 'slug', 'languagecode', 'baseid')
    list_filter = ('languagecode',)
    search_fields = ('name', 'slug')

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ('code', 'state', 'active', 'subtotal', 'orderplacedat')
    list_filter = ('state', 'active', 'orderplacedat')
    search_fields = ('code', 'customerid__emailaddress')

@admin.register(OrderLine)
class OrderLineAdmin(ModelAdmin):
    list_display = ('orderid', 'productvariantid', 'quantity', 'listprice')
    list_filter = ('orderid',)
    search_fields = ('orderid__code', 'productvariantid__sku')

@admin.register(Customer)
class CustomerAdmin(ModelAdmin):
    list_display = ('emailaddress', 'firstname', 'lastname', 'createdat')
    list_filter = ('createdat',)
    search_fields = ('emailaddress', 'firstname', 'lastname')

@admin.register(Asset)
class AssetAdmin(ModelAdmin):
    list_display = ('name', 'type', 'mimetype', 'filesize', 'preview')
    list_filter = ('type', 'mimetype')
    search_fields = ('name',)

@admin.register(Address)
class AddressAdmin(ModelAdmin):
    list_display = ('fullname', 'city', 'province', 'postalcode', 'customerid')
    list_filter = ('city', 'province')
    search_fields = ('fullname', 'city')

@admin.register(Administrator)
class AdministratorAdmin(ModelAdmin):
    list_display = ('emailaddress', 'firstname', 'lastname', 'userid')
    search_fields = ('emailaddress', 'firstname', 'lastname')

@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ('identifier', 'verified', 'lastlogin', 'createdat')
    list_filter = ('verified', 'createdat')
    search_fields = ('identifier',)

@admin.register(Payment)
class PaymentAdmin(ModelAdmin):
    list_display = ('method', 'state', 'amount', 'orderid', 'transactionid')
    list_filter = ('method', 'state')
    search_fields = ('transactionid', 'orderid__code')

@admin.register(PaymentMethod)
class PaymentMethodAdmin(ModelAdmin):
    list_display = ('code', 'enabled', 'createdat')
    list_filter = ('enabled',)
    search_fields = ('code',)

@admin.register(ShippingMethod)
class ShippingMethodAdmin(ModelAdmin):
    list_display = ('code', 'createdat')
    search_fields = ('code',)

@admin.register(Promotion)
class PromotionAdmin(ModelAdmin):
    list_display = ('couponcode', 'enabled', 'startsat', 'endsat')
    list_filter = ('enabled',)
    search_fields = ('couponcode',)

@admin.register(Refund)
class RefundAdmin(ModelAdmin):
    list_display = ('method', 'state', 'total', 'paymentid', 'transactionid')
    list_filter = ('state',)
    search_fields = ('transactionid',)

@admin.register(Channel)
class ChannelAdmin(ModelAdmin):
    list_display = ('code', 'token', 'defaultcurrencycode')
    search_fields = ('code', 'token')

@admin.register(TaxCategory)
class TaxCategoryAdmin(ModelAdmin):
    list_display = ('name', 'isdefault')
    list_filter = ('isdefault',)

@admin.register(TaxRate)
class TaxRateAdmin(ModelAdmin):
    list_display = ('name', 'enabled', 'value', 'categoryid')
    list_filter = ('enabled', 'categoryid')

@admin.register(Zone)
class ZoneAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Seller)
class SellerAdmin(ModelAdmin):
    list_display = ('name', 'createdat')
    search_fields = ('name',)

@admin.register(GlobalSettings)
class GlobalSettingsAdmin(ModelAdmin):
    list_display = ('trackinventory', 'outofstockthreshold')

@admin.register(Facet)
class FacetAdmin(ModelAdmin):
    list_display = ('id', 'isprivate', 'createdat')
    list_filter = ('isprivate',)

@admin.register(FacetTranslation)
class FacetTranslationAdmin(ModelAdmin):
    list_display = ('name', 'languagecode', 'baseid')
    list_filter = ('languagecode',)
    search_fields = ('name',)

@admin.register(FacetValue)
class FacetValueAdmin(ModelAdmin):
    list_display = ('id', 'facetid', 'createdat')
    list_filter = ('facetid',)

@admin.register(FacetValueTranslation)
class FacetValueTranslationAdmin(ModelAdmin):
    list_display = ('name', 'languagecode', 'baseid')
    list_filter = ('languagecode',)
    search_fields = ('name',)

@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('value',)
    search_fields = ('value',)

@admin.register(StockLocation)
class StockLocationAdmin(ModelAdmin):
    list_display = ('name', 'description', 'createdat')
    list_filter = ('createdat',)
    search_fields = ('name', 'description')

@admin.register(StockLevel)
class StockLevelAdmin(ModelAdmin):
    list_display = ('productvariantid', 'stocklocationid', 'stockonhand', 'updatedat')
    list_filter = ('stocklocationid', 'updatedat')
    search_fields = ('productvariantid__sku',)

@admin.register(Fulfillment)
class FulfillmentAdmin(ModelAdmin):
    list_display = ('method', 'state', 'trackingcode', 'createdat')
    list_filter = ('state',)
    search_fields = ('trackingcode',)

@admin.register(HistoryEntry)
class HistoryEntryAdmin(ModelAdmin):
    list_display = ('type', 'administratorid', 'customerid', 'orderid', 'createdat')
    list_filter = ('type', 'createdat')
    search_fields = ('data',)

@admin.register(Role)
class RoleAdmin(ModelAdmin):
    list_display = ('code', 'description')
    search_fields = ('code',)

@admin.register(Region)
class RegionAdmin(ModelAdmin):
    list_display = ('id', 'enabled', 'type')
    list_filter = ('enabled', 'type')

@admin.register(RegionTranslation)
class RegionTranslationAdmin(ModelAdmin):
    list_display = ('name', 'languagecode', 'baseid')
    list_filter = ('languagecode',)
    search_fields = ('name',)

# Register minor/join tables if needed, or skip for cleaner UI
# admin.site.register([AssetChannelsChannel, AssetTagsTag, ...])

