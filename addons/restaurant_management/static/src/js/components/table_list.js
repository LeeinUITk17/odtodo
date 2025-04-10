/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class TableList extends Component {
    static template = "restaurant_management.TableList";
    static props = {
        tables: { type: Array, element: Object },
        selectedTable: { type: [Object, null], optional: true },
        onSelectTable: { type: Function },
    };

    selectTable(table) {
        this.props.onSelectTable(table);
    }
}

registry.category("components").add("TableList", TableList);
