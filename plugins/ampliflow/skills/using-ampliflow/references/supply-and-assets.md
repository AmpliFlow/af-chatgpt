# Supply and assets

Load this reference for suppliers, supplier contacts, items, item types, equipment, purchase orders, or purchase-order lines.

## Route

- `ampliflow_suppliers`: supplier identity, contacts, options, and lifecycle.
- `ampliflow_items`: item identity, item types, options, and lifecycle.
- `ampliflow_purchase_orders`: purchase orders, supplier association, lines, line statuses, delivery information, and lifecycle.
- `ampliflow_equipment`: equipment records, options, and lifecycle.
- `ampliflow_controls`: control relationships only after equipment or another current result supplies an explicit control link.

## Relationships and order

1. Resolve the supplier before supplier contacts or supplier-scoped purchase orders.
2. Resolve item types and items before interpreting purchase-order lines.
3. Resolve a purchase order before its lines and line statuses. Keep order status and line status separate.
4. Preserve the exact supplier, contact, item, and order refs returned with each relationship.
5. Treat equipment as a managed asset, not as an item, unless AmpliFlow explicitly links the records.

## Interpretation

- A purchase order links a supplier to one or more item lines; it does not prove receipt, acceptance, or supplier performance.
- Estimated delivery is not actual delivery.
- Missing supplier contact does not mean the supplier is missing.
- A control linked to equipment records governance context, not proof that the equipment is compliant or effective.
