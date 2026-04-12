from unfold.admin import ModelAdmin, TabularInline
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

# ─── Admin Branding ───────────────────────────────────────────────────────────
admin.site.site_header = "e-sahulat Administration"
admin.site.site_title  = "e-sahulat Admin Portal"
admin.site.index_title = "Welcome to e-sahulat Management Dashboard"

# Fields to always exclude from add/change forms across all admins
_TS_FIELDS = ('createdat', 'updatedat')


# ─── Merchant ────────────────────────────────────────────────────────────────
@admin.register(MerchantProfile)
class MerchantProfileAdmin(ModelAdmin):
    list_display  = ('user', 'merchant_type', 'ntn', 'cnic', 'is_verified')
    list_filter   = ('merchant_type', 'is_verified')
    search_fields = ('user__identifier', 'ntn', 'cnic')
    exclude       = ('created_at',)


# ─── Products ────────────────────────────────────────────────────────────────
@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display  = ('id', 'enabled')
    list_filter   = ('enabled',)
    search_fields = ('id',)
    exclude       = _TS_FIELDS


@admin.register(ProductTranslation)
class ProductTranslationAdmin(ModelAdmin):
    list_display  = ('name', 'slug', 'languagecode', 'baseid')
    list_filter   = ('languagecode',)
    search_fields = ('name', 'slug')
    exclude       = _TS_FIELDS


@admin.register(ProductVariant)
class ProductVariantAdmin(ModelAdmin):
    list_display  = ('sku', 'productid', 'enabled', 'trackinventory')
    list_filter   = ('enabled', 'trackinventory')
    search_fields = ('sku',)
    exclude       = _TS_FIELDS


@admin.register(ProductVariantTranslation)
class ProductVariantTranslationAdmin(ModelAdmin):
    list_display  = ('name', 'languagecode', 'baseid')
    list_filter   = ('languagecode',)
    search_fields = ('name',)
    exclude       = _TS_FIELDS


@admin.register(ProductVariantPrice)
class ProductVariantPriceAdmin(ModelAdmin):
    list_display  = ('variantid', 'price', 'currencycode')
    list_filter   = ('currencycode',)
    search_fields = ('variantid__sku',)


# ─── Collections / Categories ────────────────────────────────────────────────
class CollectionTranslationInline(TabularInline):
    model         = CollectionTranslation
    extra         = 0
    fields        = ('languagecode', 'name', 'slug', 'description')
    readonly_fields = ('languagecode',)
    exclude       = _TS_FIELDS


@admin.register(Collection)
class CollectionAdmin(ModelAdmin):
    inlines       = [CollectionTranslationInline]
    list_display  = ('collection_name', 'isroot', 'isprivate', 'position', 'parentid', 'product_variant_count')
    list_filter   = ('isroot', 'isprivate')
    search_fields = ('collectiontranslation__name', 'collectiontranslation__slug')
    ordering      = ('isroot', 'position')
    exclude       = _TS_FIELDS

    def collection_name(self, obj):
        t = obj.collectiontranslation_set.filter(languagecode='en').first()
        return t.name if t else f"Collection #{obj.id}"
    collection_name.short_description = 'Name'

    def product_variant_count(self, obj):
        return CollectionProductVariantsProductVariant.objects.filter(collectionid=obj).count()
    product_variant_count.short_description = 'Variants'


@admin.register(CollectionTranslation)
class CollectionTranslationAdmin(ModelAdmin):
    list_display  = ('name', 'slug', 'languagecode', 'baseid')
    list_filter   = ('languagecode',)
    search_fields = ('name', 'slug')
    exclude       = _TS_FIELDS


# ─── Orders ──────────────────────────────────────────────────────────────────
@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display  = ('code', 'state', 'active', 'subtotal', 'orderplacedat')
    list_filter   = ('state', 'active')
    search_fields = ('code', 'customerid__emailaddress')
    exclude       = _TS_FIELDS


@admin.register(OrderLine)
class OrderLineAdmin(ModelAdmin):
    list_display  = ('orderid', 'productvariantid', 'quantity', 'listprice')
    list_filter   = ('orderid',)
    search_fields = ('orderid__code', 'productvariantid__sku')
    exclude       = _TS_FIELDS


# ─── Customers ───────────────────────────────────────────────────────────────
@admin.register(Customer)
class CustomerAdmin(ModelAdmin):
    list_display  = ('emailaddress', 'firstname', 'lastname')
    list_filter   = ()
    search_fields = ('emailaddress', 'firstname', 'lastname')
    exclude       = _TS_FIELDS


# ─── Assets ──────────────────────────────────────────────────────────────────
@admin.register(Asset)
class AssetAdmin(ModelAdmin):
    list_display  = ('name', 'type', 'mimetype', 'filesize', 'preview')
    list_filter   = ('type', 'mimetype')
    search_fields = ('name',)
    exclude       = _TS_FIELDS


# ─── Address ─────────────────────────────────────────────────────────────────
@admin.register(Address)
class AddressAdmin(ModelAdmin):
    list_display  = ('fullname', 'city', 'province', 'postalcode', 'customerid')
    list_filter   = ('city', 'province')
    search_fields = ('fullname', 'city')
    exclude       = _TS_FIELDS


# ─── Staff / Users ───────────────────────────────────────────────────────────
@admin.register(Administrator)
class AdministratorAdmin(ModelAdmin):
    list_display  = ('emailaddress', 'firstname', 'lastname', 'userid')
    search_fields = ('emailaddress', 'firstname', 'lastname')
    exclude       = _TS_FIELDS


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display  = ('identifier', 'verified', 'lastlogin')
    list_filter   = ('verified',)
    search_fields = ('identifier',)
    exclude       = _TS_FIELDS


# ─── Payments ────────────────────────────────────────────────────────────────
@admin.register(Payment)
class PaymentAdmin(ModelAdmin):
    list_display  = ('method', 'state', 'amount', 'orderid', 'transactionid')
    list_filter   = ('method', 'state')
    search_fields = ('transactionid', 'orderid__code')
    exclude       = _TS_FIELDS


@admin.register(PaymentMethod)
class PaymentMethodAdmin(ModelAdmin):
    list_display  = ('code', 'enabled')
    list_filter   = ('enabled',)
    search_fields = ('code',)
    exclude       = _TS_FIELDS


# ─── Shipping ────────────────────────────────────────────────────────────────
@admin.register(ShippingMethod)
class ShippingMethodAdmin(ModelAdmin):
    list_display  = ('code', 'fulfillmenthandlercode')
    search_fields = ('code',)
    exclude       = _TS_FIELDS + ('deletedat',)


# ─── Promotions ──────────────────────────────────────────────────────────────
@admin.register(Promotion)
class PromotionAdmin(ModelAdmin):
    list_display  = ('couponcode', 'enabled', 'startsat', 'endsat')
    list_filter   = ('enabled',)
    search_fields = ('couponcode',)
    exclude       = _TS_FIELDS + ('deletedat',)


# ─── Refunds ─────────────────────────────────────────────────────────────────
@admin.register(Refund)
class RefundAdmin(ModelAdmin):
    list_display  = ('method', 'state', 'total', 'paymentid', 'transactionid')
    list_filter   = ('state',)
    search_fields = ('transactionid',)
    exclude       = _TS_FIELDS


# ─── Channels ────────────────────────────────────────────────────────────────
@admin.register(Channel)
class ChannelAdmin(ModelAdmin):
    list_display  = ('code', 'token', 'defaultcurrencycode')
    search_fields = ('code', 'token')
    exclude       = _TS_FIELDS


# ─── Tax ─────────────────────────────────────────────────────────────────────
@admin.register(TaxCategory)
class TaxCategoryAdmin(ModelAdmin):
    list_display  = ('name', 'isdefault')
    list_filter   = ('isdefault',)
    exclude       = _TS_FIELDS


@admin.register(TaxRate)
class TaxRateAdmin(ModelAdmin):
    list_display  = ('name', 'enabled', 'value', 'categoryid')
    list_filter   = ('enabled', 'categoryid')
    exclude       = _TS_FIELDS


# ─── Zones / Regions ─────────────────────────────────────────────────────────
@admin.register(Zone)
class ZoneAdmin(ModelAdmin):
    list_display  = ('name',)
    search_fields = ('name',)
    exclude       = _TS_FIELDS


@admin.register(Region)
class RegionAdmin(ModelAdmin):
    list_display  = ('id', 'enabled', 'type')
    list_filter   = ('enabled', 'type')
    exclude       = _TS_FIELDS


@admin.register(RegionTranslation)
class RegionTranslationAdmin(ModelAdmin):
    list_display  = ('name', 'languagecode', 'baseid')
    list_filter   = ('languagecode',)
    search_fields = ('name',)
    exclude       = _TS_FIELDS


# ─── Sellers ─────────────────────────────────────────────────────────────────
@admin.register(Seller)
class SellerAdmin(ModelAdmin):
    list_display  = ('name',)
    search_fields = ('name',)
    exclude       = _TS_FIELDS + ('deletedat',)


# ─── Global Settings ─────────────────────────────────────────────────────────
@admin.register(GlobalSettings)
class GlobalSettingsAdmin(ModelAdmin):
    list_display  = ('trackinventory', 'outofstockthreshold')
    exclude       = _TS_FIELDS


# ─── Facets ──────────────────────────────────────────────────────────────────
@admin.register(Facet)
class FacetAdmin(ModelAdmin):
    list_display  = ('id', 'isprivate')
    list_filter   = ('isprivate',)
    exclude       = _TS_FIELDS + ('deletedat',)


@admin.register(FacetTranslation)
class FacetTranslationAdmin(ModelAdmin):
    list_display  = ('name', 'languagecode', 'baseid')
    list_filter   = ('languagecode',)
    search_fields = ('name',)
    exclude       = _TS_FIELDS


@admin.register(FacetValue)
class FacetValueAdmin(ModelAdmin):
    list_display  = ('id', 'facetid')
    list_filter   = ('facetid',)
    exclude       = _TS_FIELDS + ('deletedat',)


@admin.register(FacetValueTranslation)
class FacetValueTranslationAdmin(ModelAdmin):
    list_display  = ('name', 'languagecode', 'baseid')
    list_filter   = ('languagecode',)
    search_fields = ('name',)
    exclude       = _TS_FIELDS


# ─── Tags ────────────────────────────────────────────────────────────────────
@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display  = ('value',)
    search_fields = ('value',)
    exclude       = _TS_FIELDS


# ─── Stock ───────────────────────────────────────────────────────────────────
@admin.register(StockLocation)
class StockLocationAdmin(ModelAdmin):
    list_display  = ('name', 'description')
    search_fields = ('name', 'description')
    exclude       = _TS_FIELDS


@admin.register(StockLevel)
class StockLevelAdmin(ModelAdmin):
    list_display  = ('productvariantid', 'stocklocationid', 'stockonhand', 'stockallocated')
    list_filter   = ('stocklocationid',)
    search_fields = ('productvariantid__sku',)
    exclude       = _TS_FIELDS


# ─── Fulfillments ────────────────────────────────────────────────────────────
@admin.register(Fulfillment)
class FulfillmentAdmin(ModelAdmin):
    list_display  = ('method', 'state', 'trackingcode')
    list_filter   = ('state',)
    search_fields = ('trackingcode',)
    exclude       = _TS_FIELDS


# ─── History ─────────────────────────────────────────────────────────────────
@admin.register(HistoryEntry)
class HistoryEntryAdmin(ModelAdmin):
    list_display  = ('type', 'administratorid', 'customerid', 'orderid')
    list_filter   = ('type',)
    search_fields = ('data',)
    exclude       = _TS_FIELDS


# ─── Roles ───────────────────────────────────────────────────────────────────
@admin.register(Role)
class RoleAdmin(ModelAdmin):
    list_display  = ('code', 'description')
    search_fields = ('code',)
    exclude       = _TS_FIELDS


# Register minor/join tables if needed, or skip for cleaner UI
# admin.site.register([AssetChannelsChannel, AssetTagsTag, ...])
