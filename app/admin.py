from unfold.admin import ModelAdmin, TabularInline, StackedInline
from unfold.decorators import display
from unfold.contrib.filters.admin import DropdownFilter, ChoicesDropdownFilter, RelatedDropdownFilter
from django.contrib import admin
from django.utils.safestring import mark_safe
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
admin.site.site_header = "mukhtaleefweart Administration"
admin.site.site_title  = "mukhtaleefweart Admin Portal"
admin.site.index_title = "Welcome to mukhtaleefweart Management Dashboard"

# Fields to always exclude from add/change forms across all admins
_TS_FIELDS = ('createdat', 'updatedat')

def format_currency(amount):
    """Helper to format currency in PKR"""
    if amount is None:
        return mark_safe('<span class="text-gray-400">₨ 0.00</span>')
    # Amount is likely in cents/minor units in Vendure/Database
    val = float(amount) / 100 if abs(float(amount)) > 1000 else float(amount)
    return f"₨ {val:,.2f}"

from django.utils import timezone
from .utils import send_merchant_welcome_email

# ─── Merchant ────────────────────────────────────────────────────────────────
@admin.register(MerchantProfile)
class MerchantProfileAdmin(ModelAdmin):
    list_display  = ('user', 'merchant_type', 'ntn', 'cnic', 'display_status', 'display_docs')
    list_filter   = (
        ('merchant_type', ChoicesDropdownFilter),
        'is_verified',
    )
    search_fields = ('user__identifier', 'ntn', 'cnic')
    exclude       = ('created_at',)
    actions       = ['verify_merchants']

    @display(description="Status")
    def display_status(self, obj):
        return obj.is_verified

    display_status.label = {True: "Verified", False: "Pending"}
    display_status.color = {True: "success", False: "warning"}

    @display(description="Documents")
    def display_docs(self, obj):
        from django.urls import reverse
        docs = []
        if obj.cnic_front:
            url = reverse('serve_merchant_document', args=[obj.id, 'cnic_front'])
            docs.append(f'<a href="{url}" target="_blank" class="text-primary-600 font-medium hover:underline">CNIC-F</a>')
        if obj.cnic_back:
            url = reverse('serve_merchant_document', args=[obj.id, 'cnic_back'])
            docs.append(f'<a href="{url}" target="_blank" class="text-primary-600 font-medium hover:underline">CNIC-B</a>')
        if obj.utility_bill:
            url = reverse('serve_merchant_document', args=[obj.id, 'utility_bill'])
            docs.append(f'<a href="{url}" target="_blank" class="text-primary-600 font-medium hover:underline">Bill</a>')
        return mark_safe(" | ".join(docs)) if docs else mark_safe('<span class="text-gray-400 italic">No Docs</span>')

    @admin.action(description="Verify selected merchants")
    def verify_merchants(self, request, queryset):
        count = 0
        for merchant in queryset:
            if not merchant.is_verified:
                merchant.is_verified = True
                merchant.save()
                
                # Send welcome email
                context = {
                    'merchant_name': merchant.user.identifier,
                    'merchant_id': f"MID-{merchant.id:05d}",
                    'merchant_type': merchant.merchant_type,
                    'verification_date': timezone.now(),
                    'dashboard_url': request.build_absolute_uri('/dashboard/'),
                }
                send_merchant_welcome_email(merchant.user.identifier, context)
                count += 1
        
        self.message_user(request, f"Successfully verified {count} merchants and sent welcome emails.")


# ─── Products ────────────────────────────────────────────────────────────────
from django import forms

class ProductVariantInlineForm(forms.ModelForm):
    price = forms.DecimalField(
        label="Price (PKR)", 
        required=False, 
        max_digits=12, 
        decimal_places=2,
        help_text="Enter price in PKR. It will be converted to minor units (cents) automatically."
    )
    name = forms.CharField(
        label="Variant Name",
        required=False,
        help_text="Leave blank to use product name."
    )

    class Meta:
        model = ProductVariant
        fields = ['sku', 'name', 'price', 'enabled', 'trackinventory']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # Load price
            price_obj = self.instance.productvariantprice_set.first()
            if price_obj:
                self.fields['price'].initial = float(price_obj.price) / 100
            
            # Load name
            trans_obj = self.instance.productvarianttranslation_set.filter(languagecode='en').first()
            if trans_obj:
                self.fields['name'].initial = trans_obj.name

    def save(self, commit=True):
        instance = super().save(commit=commit)
        price_val = self.cleaned_data.get('price')
        name_val = self.cleaned_data.get('name')

        if commit:
            # Handle Price
            if price_val is not None:
                minor_price = int(price_val * 100)
                ProductVariantPrice.objects.update_or_create(
                    variantid=instance,
                    defaults={'price': minor_price, 'currencycode': 'PKR'}
                )
            
            # Handle Translation
            if name_val:
                ProductVariantTranslation.objects.update_or_create(
                    baseid=instance,
                    languagecode='en',
                    defaults={'name': name_val}
                )
        return instance

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'featuredassetid' in self.fields:
            self.fields['featuredassetid'].label = "Image Upload"

class ProductTranslationInline(StackedInline):
    model = ProductTranslation
    extra = 1
    fields = ('name', 'description')
    tab = False
    classes = ['unfold-stacked-inline-compressed']

class ProductAssetInline(TabularInline):
    model = ProductAsset
    extra = 3
    exclude = _TS_FIELDS
    autocomplete_fields = ('assetid',)
    tab = True

class ProductVariantInline(StackedInline):
    model = ProductVariant
    form = ProductVariantInlineForm
    extra = 1
    show_change_link = True
    exclude = _TS_FIELDS + ('deletedat',)
    fields = (('sku', 'name', 'price'), ('enabled', 'trackinventory', 'taxcategoryid'))
    tab = True
    classes = ['unfold-stacked-inline-compressed']

class ProductChannelsChannelInline(TabularInline):
    model = ProductChannelsChannel
    extra = 1
    tab = True

class PerPageFilter(admin.SimpleListFilter):
    title = 'Items per page'
    parameter_name = 'per_page'

    def lookups(self, request, model_admin):
        return (
            ('10', '10'),
            ('20', '20'),
            ('50', '50'),
        )

    def queryset(self, request, queryset):
        return queryset

from django.db.models import Count, Min, Max, Prefetch

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    form = ProductAdminForm
    list_display  = ('display_image', 'product_name', 'display_enabled', 'variant_count', 'display_price_range', 'display_actions')
    list_filter   = ('enabled', PerPageFilter)
    search_fields = ('producttranslation__name',)
    list_per_page = 20
    list_select_related = ('featuredassetid',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Solve N+1 for translations and pricing
        queryset = queryset.annotate(
            _variant_count=Count('productvariant', distinct=True),
            _min_price=Min('productvariant__productvariantprice__price'),
            _max_price=Max('productvariant__productvariantprice__price'),
        ).prefetch_related(
            Prefetch(
                'producttranslation_set',
                queryset=ProductTranslation.objects.filter(languagecode='en'),
                to_attr='en_translations'
            )
        )
        return queryset

    @display(description="Image")
    def display_image(self, obj):
        if obj.featuredassetid and obj.featuredassetid.preview:
            return mark_safe(f'<img src="{obj.featuredassetid.preview}" class="w-10 h-10 object-cover rounded shadow-sm" />')
        return mark_safe('<div class="w-10 h-10 bg-gray-100 rounded flex items-center justify-center text-gray-400">?</div>')

    @display(description="Name")
    def product_name(self, obj):
        if hasattr(obj, 'en_translations') and obj.en_translations:
            return obj.en_translations[0].name
        return f"Product #{obj.id}"

    @display(description="Enabled", boolean=True)
    def display_enabled(self, obj):
        return obj.enabled

    @display(description="Variants", ordering='_variant_count')
    def variant_count(self, obj):
        return obj._variant_count

    @display(description="Price Range", ordering='_min_price')
    def display_price_range(self, obj):
        min_p = obj._min_price
        max_p = obj._max_price
        if min_p is None: return "N/A"
        if min_p == max_p: return format_currency(min_p)
        return f"{format_currency(min_p)} - {format_currency(max_p)}"

    inlines       = [
        ProductTranslationInline, 
        ProductAssetInline, 
        ProductVariantInline,
        ProductChannelsChannelInline
    ]
    exclude       = _TS_FIELDS + ('deletedat',)
    raw_id_fields = ('featuredassetid',)
    readonly_fields = ('selected_image_display',)
    
    fieldsets = (
        ("General Status", {
            "fields": (("enabled", "featuredassetid", "selected_image_display"),),
            "classes": ["unfold-fieldset-compact"],
        }),
    )

    @display(description="Selected Image")
    def selected_image_display(self, obj):
        if obj.featuredassetid:
            url = obj.featuredassetid.preview
            if not (url.startswith('http') or url.startswith('/')):
                from django.conf import settings
                url = f"{settings.MEDIA_URL}{url}"
            return mark_safe(f'<div class="flex items-center gap-2"><img src="{url}" class="w-10 h-10 object-cover rounded shadow-sm" /> <span>{obj.featuredassetid.name}</span></div>')
        return "No image selected"

    @display(description="Actions")
    def display_actions(self, obj):
        from django.urls import reverse
        change_url = reverse('admin:app_product_change', args=[obj.pk])
        delete_url = reverse('admin:app_product_delete', args=[obj.pk])
        
        return mark_safe(f'''
            <div class="flex items-center gap-2">
                <a href="{change_url}" class="text-primary-600 hover:text-primary-700 transition-colors" title="Edit">
                    <span class="material-symbols-outlined !text-[20px]">edit_square</span>
                </a>
                <a href="{delete_url}" class="text-red-600 hover:text-red-700 transition-colors" title="Delete">
                    <span class="material-symbols-outlined !text-[20px]">delete</span>
                </a>
            </div>
        ''')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:
            from .models import Channel
            default_channel = Channel.objects.filter(id=1).first()
            if default_channel:
                ProductChannelsChannel.objects.get_or_create(
                    productid=obj,
                    channelid=default_channel
                )


class ProductVariantTranslationInline(TabularInline):
    model = ProductVariantTranslation
    extra = 1
    exclude = _TS_FIELDS

class ProductVariantPriceInline(TabularInline):
    model = ProductVariantPrice
    extra = 1
    exclude = _TS_FIELDS

class ProductVariantAssetInline(TabularInline):
    model = ProductVariantAsset
    extra = 1
    exclude = _TS_FIELDS
    autocomplete_fields = ('assetid',)

@admin.register(ProductVariant)
class ProductVariantAdmin(ModelAdmin):
    list_display  = ('sku', 'variant_name', 'display_price', 'display_enabled', 'trackinventory')
    list_filter   = (
        'enabled',
        ('trackinventory', ChoicesDropdownFilter),
        ('productid', RelatedDropdownFilter),
    )
    search_fields = ('sku', 'productvarianttranslation__name')
    inlines       = [ProductVariantTranslationInline, ProductVariantPriceInline, ProductVariantAssetInline]
    exclude       = _TS_FIELDS + ('deletedat',)
    autocomplete_fields = ('featuredassetid', 'productid')
    actions       = ['duplicate_variants']

    @display(description="Name")
    def variant_name(self, obj):
        t = obj.productvarianttranslation_set.filter(languagecode='en').first()
        return t.name if t else f"Variant #{obj.id}"

    @display(description="Price")
    def display_price(self, obj):
        price = obj.productvariantprice_set.first()
        return format_currency(price.price) if price else "N/A"

    @display(description="Enabled", boolean=True)
    def display_enabled(self, obj):
        return obj.enabled

    @admin.action(description="Duplicate selected variants")
    def duplicate_variants(self, request, queryset):
        for variant in queryset:
            original_pk = variant.pk
            variant.pk = None
            variant.sku = f"{variant.sku}-COPY"
            variant.save()
            # Copy related prices
            for price in ProductVariantPrice.objects.filter(variantid=original_pk):
                price.pk = None
                price.variantid = variant
                price.save()
            # Copy related translations
            for trans in ProductVariantTranslation.objects.filter(baseid=original_pk):
                trans.pk = None
                trans.baseid = variant
                trans.save()
        self.message_user(request, f"Duplicated {queryset.count()} variants.")


# ─── Collections / Categories ────────────────────────────────────────────────
class CollectionTranslationInline(TabularInline):
    model         = CollectionTranslation
    extra         = 0
    fields        = ('name', 'slug', 'description')
    exclude       = _TS_FIELDS


@admin.register(Collection)
class CollectionAdmin(ModelAdmin):
    inlines       = [CollectionTranslationInline]
    list_display  = ('collection_name', 'isroot', 'isprivate', 'position', 'parentid', 'product_variant_count')
    list_filter   = (
        'isroot',
        'isprivate',
    )
    search_fields = ('collectiontranslation__name', 'collectiontranslation__slug')
    ordering      = ('isroot', 'position')
    exclude       = _TS_FIELDS

    @display(description="Name")
    def collection_name(self, obj):
        t = obj.collectiontranslation_set.filter(languagecode='en').first()
        return t.name if t else f"Collection #{obj.id}"

    @display(description="Variants")
    def product_variant_count(self, obj):
        return CollectionProductVariantsProductVariant.objects.filter(collectionid=obj).count()


@admin.register(CollectionTranslation)
class CollectionTranslationAdmin(ModelAdmin):
    list_display  = ('name', 'display_description', 'slug', 'languagecode', 'baseid')
    list_filter   = (('languagecode', ChoicesDropdownFilter),)
    search_fields = ('name', 'slug')
    exclude       = _TS_FIELDS

    @display(description="Description")
    def display_description(self, obj):
        from django.template.defaultfilters import truncatechars
        return truncatechars(obj.description, 50)


# ─── Orders ──────────────────────────────────────────────────────────────────
@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display  = ('code', 'display_customer', 'display_state', 'active', 'display_total', 'orderplacedat')
    list_filter   = (
        ('state', ChoicesDropdownFilter),
        'active',
        'orderplacedat',
    )
    search_fields = ('code', 'customerid__emailaddress')
    exclude       = _TS_FIELDS

    @display(description="Customer")
    def display_customer(self, obj):
        if obj.customerid:
            return f"{obj.customerid.firstname} {obj.customerid.lastname} ({obj.customerid.emailaddress})"
        return mark_safe('<span class="text-gray-400">Guest</span>')

    @display(description="State")
    def display_state(self, obj):
        return obj.state

    display_state.label = {
        "PaymentSettled": "Settled",
        "Shipped": "Shipped",
        "Delivered": "Delivered",
        "Cancelled": "Cancelled",
        "AddingItems": "Draft",
        "ArrangingPayment": "Pending Payment",
    }
    display_state.color = {
        "PaymentSettled": "success",
        "Shipped": "info",
        "Delivered": "success",
        "Cancelled": "danger",
        "AddingItems": "warning",
        "ArrangingPayment": "warning",
    }

    @display(description="Total")
    def display_total(self, obj):
        return format_currency(obj.subtotal)


@admin.register(OrderLine)
class OrderLineAdmin(ModelAdmin):
    list_display  = ('orderid', 'productvariantid', 'quantity', 'display_price')
    list_filter   = (('orderid', RelatedDropdownFilter),)
    search_fields = ('orderid__code', 'productvariantid__sku')
    exclude       = _TS_FIELDS

    @display(description="Price")
    def display_price(self, obj):
        return format_currency(obj.listprice)


# ─── Customers ───────────────────────────────────────────────────────────────
@admin.register(Customer)
class CustomerAdmin(ModelAdmin):
    list_display  = ('emailaddress', 'firstname', 'lastname')
    list_filter   = ()
    search_fields = ('emailaddress', 'firstname', 'lastname')
    exclude       = _TS_FIELDS


# ─── Assets ──────────────────────────────────────────────────────────────────
import os
from django.conf import settings
from django.core.files.storage import default_storage

class AssetAdminForm(forms.ModelForm):
    file_upload = forms.FileField(
        required=False, 
        label="Upload New File", 
        help_text="Upload an image to automatically set source and metadata.",
        widget=forms.ClearableFileInput(attrs={
            'class': 'unfold-file-input border rounded-lg text-black cursor-pointer px-3 py-2',
        })
    )

    class Meta: 
        model = Asset
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get('file_upload')
        if file and not cleaned_data.get('name'):
            # Set name early so model.clean() doesn't fail
            self.instance.name = file.name
            cleaned_data['name'] = file.name
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        file = self.cleaned_data.get('file_upload')
        
        if file:
            import io
            from PIL import Image
            from django.core.files.base import ContentFile
            
            # 1. Open image
            img = Image.open(file)
            
            # 2. Convert to RGB if necessary
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            # 3. Compress
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=75, optimize=True)
            output.seek(0)
            
            # 4. Create ContentFile
            optimized_file = ContentFile(output.read(), name=os.path.splitext(file.name)[0] + '.jpg')
            
            # 5. Save using default_storage (Cloudinary)
            # Cloudinary storage returns the public URL or the path that can be converted to a URL
            filename = default_storage.save(f"assets/{optimized_file.name}", optimized_file)
            
            # 6. Get the public URL from the storage
            file_url = default_storage.url(filename)
            
            # Update source and preview with the ACTUAL cloud URL
            instance.source = file_url
            instance.preview = file_url
            instance.name = optimized_file.name
            
            # Ensure required fields are not null to prevent IntegrityError
            if not instance.type:
                instance.type = 'IMAGE'
            if not instance.mimetype:
                instance.mimetype = 'image/jpeg'
            
        if commit:
            instance.save()
        return instance

@admin.register(Asset)
class AssetAdmin(ModelAdmin):
    form = AssetAdminForm
    list_display  = ('display_preview', 'name', 'type', 'mimetype', 'display_size', 'display_actions')
    list_display_links = ('display_preview', 'name') # Make preview clickable too
    list_filter   = (
        ('type', ChoicesDropdownFilter),
        ('mimetype', ChoicesDropdownFilter),
    )
    search_fields = ('name',)
    exclude       = _TS_FIELDS
    readonly_fields = ('width', 'height', 'filesize', 'mimetype')
    
    class Media:
        css = {
            'all': ('css/admin-grid.css',)
        }
        js = ('js/admin-loading.js',)
    
    fieldsets = (
        ("File Upload", {
            "fields": ("file_upload",),
        }),
    )

    @display(description="Actions")
    def display_actions(self, obj):
        from django.urls import reverse
        change_url = reverse('admin:app_asset_change', args=[obj.pk])
        delete_url = reverse('admin:app_asset_delete', args=[obj.pk])
        
        return mark_safe(f'''
            <div class="flex items-center gap-2">
                <a href="{change_url}" class="text-primary-600 hover:text-primary-700 transition-colors" title="Edit">
                    <span class="material-symbols-outlined !text-[20px]">edit_square</span>
                </a>
                <a href="{delete_url}" class="text-red-600 hover:text-red-700 transition-colors" title="Delete">
                    <span class="material-symbols-outlined !text-[20px]">delete</span>
                </a>
            </div>
        ''')

    @display(description="Preview")
    def display_preview(self, obj):
        if obj.preview:
            url = obj.preview
            # If it's a relative path starting with 'assets/', prepend MEDIA_URL
            if not url.startswith(('http', '/', 'https')):
                url = f"{settings.MEDIA_URL}{url}"
            return mark_safe(f'<img src="{url}" class="w-10 h-10 object-cover rounded shadow-sm" />')
        return "No Preview"

    @display(description="Size")
    def display_size(self, obj):
        if obj.filesize:
            return f"{obj.filesize / 1024:.1f} KB"
        return "0 KB"


# ─── Address ─────────────────────────────────────────────────────────────────
@admin.register(Address)
class AddressAdmin(ModelAdmin):
    list_display  = ('fullname', 'city', 'province', 'postalcode', 'customerid')
    list_filter   = (
        ('city', ChoicesDropdownFilter),
        ('province', ChoicesDropdownFilter),
    )
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
    list_display  = ('identifier', 'display_verified', 'lastlogin')
    list_filter   = ('verified',)
    search_fields = ('identifier',)
    exclude       = _TS_FIELDS

    @display(description="Verified", boolean=True)
    def display_verified(self, obj):
        return obj.verified


# ─── Payments ────────────────────────────────────────────────────────────────
@admin.register(Payment)
class PaymentAdmin(ModelAdmin):
    list_display  = ('transactionid', 'method', 'display_state', 'display_amount', 'orderid')
    list_filter   = (
        ('method', ChoicesDropdownFilter),
        ('state', ChoicesDropdownFilter),
    )
    search_fields = ('transactionid', 'orderid__code')
    exclude       = _TS_FIELDS

    @display(description="State")
    def display_state(self, obj):
        return obj.state

    display_state.label = {
        "Settled": "Settled",
        "Authorized": "Authorized",
        "Declined": "Declined",
        "Cancelled": "Cancelled",
    }
    display_state.color = {
        "Settled": "success",
        "Authorized": "info",
        "Declined": "danger",
        "Cancelled": "warning",
    }

    @display(description="Amount")
    def display_amount(self, obj):
        return format_currency(obj.amount)


@admin.register(PaymentMethod)
class PaymentMethodAdmin(ModelAdmin):
    list_display  = ('code', 'display_enabled')
    list_filter   = ('enabled',)
    search_fields = ('code',)
    exclude       = _TS_FIELDS

    @display(description="Enabled", boolean=True)
    def display_enabled(self, obj):
        return obj.enabled


# ─── Shipping ────────────────────────────────────────────────────────────────
@admin.register(ShippingMethod)
class ShippingMethodAdmin(ModelAdmin):
    list_display  = ('code', 'fulfillmenthandlercode')
    search_fields = ('code',)
    exclude       = _TS_FIELDS + ('deletedat',)


# ─── Promotions ──────────────────────────────────────────────────────────────
@admin.register(Promotion)
class PromotionAdmin(ModelAdmin):
    list_display  = ('couponcode', 'display_enabled', 'startsat', 'endsat')
    list_filter   = ('enabled',)
    search_fields = ('couponcode',)
    exclude       = _TS_FIELDS + ('deletedat',)

    @display(description="Enabled", boolean=True)
    def display_enabled(self, obj):
        return obj.enabled


# ─── Refunds ─────────────────────────────────────────────────────────────────
@admin.register(Refund)
class RefundAdmin(ModelAdmin):
    list_display  = ('method', 'display_state', 'display_total', 'paymentid', 'transactionid')
    list_filter   = (('state', ChoicesDropdownFilter),)
    search_fields = ('transactionid',)
    exclude       = _TS_FIELDS

    @display(description="State")
    def display_state(self, obj):
        return obj.state

    display_state.label = {
        "Settled": "Settled",
        "Failed": "Failed",
        "Pending": "Pending",
    }
    display_state.color = {
        "Settled": "success",
        "Failed": "danger",
        "Pending": "warning",
    }

    @display(description="Total")
    def display_total(self, obj):
        return format_currency(obj.total)


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
    list_display  = ('name', 'display_enabled', 'value', 'categoryid')
    list_filter   = (
        'enabled',
        ('categoryid', RelatedDropdownFilter),
    )
    exclude       = _TS_FIELDS

    @display(description="Enabled", boolean=True)
    def display_enabled(self, obj):
        return obj.enabled


# ─── Zones / Regions ─────────────────────────────────────────────────────────
@admin.register(Zone)
class ZoneAdmin(ModelAdmin):
    list_display  = ('name',)
    search_fields = ('name',)
    exclude       = _TS_FIELDS


@admin.register(Region)
class RegionAdmin(ModelAdmin):
    list_display  = ('id', 'display_enabled', 'type')
    list_filter   = (
        'enabled',
        ('type', ChoicesDropdownFilter),
    )
    exclude       = _TS_FIELDS

    @display(description="Enabled", boolean=True)
    def display_enabled(self, obj):
        return obj.enabled


@admin.register(RegionTranslation)
class RegionTranslationAdmin(ModelAdmin):
    list_display  = ('name', 'languagecode', 'baseid')
    list_filter   = (('languagecode', ChoicesDropdownFilter),)
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


@admin.register(ProductTranslation)
class ProductTranslationAdmin(ModelAdmin):
    list_display = ('name', 'display_description', 'slug', 'languagecode', 'baseid')
    list_filter = (('languagecode', ChoicesDropdownFilter),)
    search_fields = ('name', 'slug')
    exclude = _TS_FIELDS

    @display(description="Description")
    def display_description(self, obj):
        from django.template.defaultfilters import truncatechars
        return truncatechars(obj.description, 50)



# ─── Facet Values ────────────────────────────────────────────────────────────
@admin.register(FacetValue)
class FacetValueAdmin(ModelAdmin):
    list_display  = ('id', 'facetid')
    list_filter   = (('facetid', RelatedDropdownFilter),)
    exclude       = _TS_FIELDS + ('deletedat',)


@admin.register(FacetValueTranslation)
class FacetValueTranslationAdmin(ModelAdmin):
    list_display  = ('name', 'languagecode', 'baseid')
    list_filter   = (('languagecode', ChoicesDropdownFilter),)
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
    list_filter   = (
        ('stocklocationid', RelatedDropdownFilter),
    )
    search_fields = ('productvariantid__sku',)
    exclude       = _TS_FIELDS


# ─── Fulfillments ────────────────────────────────────────────────────────────
@admin.register(Fulfillment)
class FulfillmentAdmin(ModelAdmin):
    list_display  = ('method', 'display_state', 'trackingcode')
    list_filter   = (('state', ChoicesDropdownFilter),)
    search_fields = ('trackingcode',)
    exclude       = _TS_FIELDS

    @display(description="State")
    def display_state(self, obj):
        return obj.state

    display_state.label = {
        "Shipped": "Shipped",
        "Delivered": "Delivered",
        "Cancelled": "Cancelled",
    }
    display_state.color = {
        "Shipped": "info",
        "Delivered": "success",
        "Cancelled": "danger",
    }

    def save_model(self, request, obj, form, change):
        if obj.state == "Shipped" and not obj.trackingcode:
            from django.contrib import messages
            messages.error(request, "Error: Tracking Code is required to mark an order as Shipped.")
            return # Prevent saving
        super().save_model(request, obj, form, change)


# ─── History ─────────────────────────────────────────────────────────────────
@admin.register(HistoryEntry)
class HistoryEntryAdmin(ModelAdmin):
    list_display  = ('type', 'administratorid', 'customerid', 'orderid')
    list_filter   = (('type', ChoicesDropdownFilter),)
    search_fields = ('data',)
    exclude       = _TS_FIELDS


# ─── Roles ───────────────────────────────────────────────────────────────────
@admin.register(Role)
class RoleAdmin(ModelAdmin):
    list_display  = ('code', 'description')
    search_fields = ('code',)
    exclude       = _TS_FIELDS
