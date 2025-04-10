/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class OrderCart extends Component {
    static template = "restaurant_management.OrderCart";
    static props = {
        orderLines: { type: Array, element: Object },
        total: { type: Number },
        selectedTable: { type: [Object, null], optional: true },
        onUpdateQty: { type: Function },
        onSendOrder: { type: Function },
    };

    updateQty(line, ev) {
        const newQty = parseInt(ev.target.value);
        if (!isNaN(newQty) && newQty >= 0 && line && this.props.onUpdateQty) {
            this.props.onUpdateQty(line, newQty);
        } else if (newQty < 0) {
            ev.target.value = line.qty;
        }
    }
}

registry.category("components").add("OrderCart", OrderCart);
