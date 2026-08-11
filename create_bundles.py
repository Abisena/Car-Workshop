import os
os.chdir("/home/chandrasudrajat/garage/sites")
import frappe
frappe.init(site="retail.localhost")
frappe.connect()

# Create non-stock parent items for bundles
parent_items = [
    ("PKT-TUNEUP", "Paket Tune Up"),
    ("PKT-OLI", "Paket Ganti Oli"),
    ("PKT-REM", "Paket Ganti Rem"),
    ("PKT-AC", "Paket Servis AC"),
    ("PKT-RADIATOR", "Paket Servis Radiator"),
]

for code, name in parent_items:
    if frappe.db.exists("Item", code):
        print("SKIP ITEM " + code)
        continue
    item = frappe.new_doc("Item")
    item.item_code = code
    item.item_name = name
    item.item_group = "Products"
    item.is_stock_item = 0
    item.stock_uom = "Unit"
    item.insert(ignore_permissions=True)
    print("CREATED ITEM " + code)

# Create Product Bundles
bundles = [
    {
        "parent": "PKT-TUNEUP",
        "desc": "Paket Tune Up Standar",
        "items": [
            ("OLI-001", 4), ("FLT-001", 1), ("FLT-002", 1),
            ("SPK-001", 4), ("JSA-001", 1),
        ]
    },
    {
        "parent": "PKT-OLI",
        "desc": "Paket Ganti Oli + Filter",
        "items": [
            ("OLI-001", 4), ("FLT-001", 1),
        ]
    },
    {
        "parent": "PKT-REM",
        "desc": "Paket Ganti Rem Depan + Belakang",
        "items": [
            ("BRK-001", 1), ("BRK-002", 1), ("OLI-004", 1),
        ]
    },
    {
        "parent": "PKT-AC",
        "desc": "Paket Servis AC",
        "items": [
            ("CLN-002", 2), ("FLT-003", 1),
        ]
    },
    {
        "parent": "PKT-RADIATOR",
        "desc": "Paket Servis Radiator",
        "items": [
            ("CLN-001", 2), ("BLT-003", 1),
        ]
    },
]

for b in bundles:
    parent = b["parent"]
    if frappe.db.exists("Product Bundle", {"new_item_code": parent}):
        print("SKIP BUNDLE " + parent)
        continue
    doc = frappe.new_doc("Product Bundle")
    doc.new_item_code = parent
    doc.description = b["desc"]
    for item_code, qty in b["items"]:
        doc.append("items", {"item_code": item_code, "qty": qty})
    doc.insert(ignore_permissions=True)
    print("CREATED BUNDLE " + doc.name + " - " + b["desc"])

# Link bundles to service types
links = {
    "TUNE UP": "PKT-TUNEUP",
    "GANTI OLI": "PKT-OLI",
    "GANTI REM": "PKT-REM",
    "SERVIS AC": "PKT-AC",
    "SERVIS RADIATOR": "PKT-RADIATOR",
}
for stype, parent_item in links.items():
    bundle_name = frappe.db.get_value("Product Bundle", {"new_item_code": parent_item}, "name")
    if bundle_name:
        frappe.db.set_value("Garage Service Type", stype, "product_bundle", bundle_name)
        print("LINKED " + stype + " -> " + bundle_name)

frappe.db.commit()
frappe.destroy()
print("DONE")
