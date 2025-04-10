/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class MenuGrid extends Component {
    static template = "restaurant_management.MenuGrid";
    static props = {
        menuItems: { type: Array, element: Object },
        categories: { type: Array, element: Object },
        onAddToCart: { type: Function },
    };

    setup() {
        this.state = useState({
            selectedCategoryId: null,
        });
    }

    get filteredMenuItems() {
        if (!this.state.selectedCategoryId) {
            return this.props.menuItems;
        }
        return this.props.menuItems.filter(
            item => item.category_uuid && item.category_uuid[0] === this.state.selectedCategoryId
        );
    }

    selectCategory(categoryId) {
        this.state.selectedCategoryId = this.state.selectedCategoryId === categoryId ? null : categoryId;
    }

    addToCart(menuItem) {
        this.props.onAddToCart(menuItem);
    }
}

registry.category("components").add("MenuGrid", MenuGrid);
