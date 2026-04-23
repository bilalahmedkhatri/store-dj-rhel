# mukhtaleefweart Admin Management Guide

This guide explains how to add and manage store data through the Django Admin panel following the project's translation-based architecture.

---

## 1. Adding a Product (Main Workflow)

Adding a product involves three main parts: the Product container, its translations (Name/Description), and its Variants (SKU/Price).

### Step-by-Step:
1.  **Go to "Products"** in the admin sidebar and click **"Add Product"**.
2.  **Basic Settings**: Toggle the `Enabled` checkbox.
3.  **Product Translations**:
    *   Find the **Product Translation Inline**.
    *   Set `Language Code` (e.g., `en`).
    *   Enter the `Name`, `Slug`, and `Description`.
4.  **Add Variants** (Optional at this stage):
    *   You can add a basic variant directly in the **Product Variant Inline**.
    *   *Note: For detailed variant setup (Price/Stock), it is better to save the product first and then edit the variant.*
5.  **Click Save**.

---

## 2. Managing Product Variants (Price & SKU)

Every product must have at least one variant to be purchasable.

### Step-by-Step:
1.  **Go to "Product Variants"**.
2.  **Select a Variant** or click **"Add Product Variant"**.
3.  **Identify Parent**: Select the parent `Product`.
4.  **Set SKU**: Enter a unique SKU (e.g., `TSHIRT-BLUE-MED`).
5.  **Variant Translations**: Add a name (e.g., "Blue T-Shirt - Medium") in the **Product Variant Translation Inline**.
6.  **Set Price**:
    *   In the **Product Variant Price Inline**, enter the `Price` (integer format: `1000` = `10.00` if using minor units, or as configured).
    *   Set the `Currency Code` (e.g., `PKR`).
7.  **Click Save**.

---

## 3. Adding Categories (Collections)

Categories are called **Collections** in this system.

### Step-by-Step:
1.  **Go to "Collections"**.
2.  **Hierarchy**:
    *   For a top-level category: Check `Is Root` and leave `Parent ID` empty.
    *   For a sub-category: Uncheck `Is Root` and select a `Parent ID`.
3.  **Translations**: In the **Collection Translation Inline**, add the `Name` and `Slug`.
4.  **Assign Products**: Use the **Collection Product Variants** section (or the join table `CollectionProductVariantsProductVariant`) to link variants to this category.

---

## 4. Managing Media (Assets)

Images are handled as **Assets** and linked to products/variants.

### Step-by-Step:
1.  **Upload Image**:
    *   Go to **"Assets"** and click **"Add Asset"**.
    *   Upload the file and give it a name.
2.  **Link to Product**:
    *   Go back to your **Product** or **Product Variant**.
    *   Find the **Product Asset Inline**.
    *   Select the asset you just uploaded.
    *   Set its `Position` (0 for main image).

---

## 5. Adding Other Data Types

### Staff & Users
*   **Step 1**: Create a **User** (set `Identifier` as their email/username).
*   **Step 2**: Create an **Administrator** profile and link it to the **User** you created.

### Merchants
*   Go to **"Merchant Profiles"**.
*   Link to an existing **User**.
*   Upload documents (CNIC, Bills) and set `Is Verified` to `True` once reviewed.

### Shipping & Payments
*   **Payment Methods**: Add the method (e.g., `payfast`). Ensure you add a `Payment Method Translation` so the name appears correctly on the frontend.
*   **Shipping Methods**: Define the method and its cost/calculator logic.

---

## 💡 Important Pro-Tips
*   **Translations are Mandatory**: If you don't add an `en` (English) translation, the product name may appear as "Product #ID" on the frontend.
*   **Slug Integrity**: Always use URL-friendly slugs (e.g., `my-cool-product`) in translations.
*   **Timestamps**: The `createdAt` and `updatedAt` fields are automatically managed and excluded from the forms for a cleaner UI.
