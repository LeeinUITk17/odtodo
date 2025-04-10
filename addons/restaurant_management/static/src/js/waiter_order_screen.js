/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState, onWillStart, useService } from "@odoo/owl";
import { OrderCart } from "./components/order_cart";
import { MenuGrid } from "./components/menu_grid";
import { TableList } from "./components/table_list";

export class WaiterOrderScreen extends Component {
    static template = "restaurant_management.WaiterOrderScreen";
    static components = { OrderCart, MenuGrid, TableList };

    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.state = useState({
            tables: [],
            menuItems: [],
            categories: [],
            selectedTable: null,
            currentOrderLines: [],
            currentTotal: 0,
            isLoading: true,
        });

        onWillStart(async () => {
            await this.loadInitialData();
            this.state.isLoading = false;
        });
    }

    async loadInitialData() {
        try {
            this.state.tables = await this.orm.searchRead(
                "restaurant_management.table",
                [['status', '=', 'available']],
                ["id", "name", "capacity", "status"]
            );

            const userBranch = await this.orm.read(
                "res.users",
                [this.env.services.user.userId],
                ["branch_id"]
            );
            const currentBranchId = userBranch.length ? userBranch[0].branch_id[0] : null;

            if (!currentBranchId) {
                this.notification.add(_t("User branch not configured! Cannot load menu."), { type: 'danger' });
                this.state.menuItems = [];
                this.state.categories = [];
                return;
            }

            const menuItemsData = await this.orm.searchRead(
                "restaurant_management.menuitem",
                [['branch_uuid', '=', currentBranchId], ['active', '=', true]],
                ["id", "name", "price", "category_uuid", "image", "currency_id"]
            );
            this.state.menuItems = menuItemsData;

            const categoryIds = [...new Set(menuItemsData.map(item => item.category_uuid?.[0]).filter(id => id))];
            if (categoryIds.length > 0) {
                this.state.categories = await this.orm.searchRead(
                    "restaurant_management.category",
                    [['id', 'in', categoryIds]],
                    ["id", "name"]
                );
            } else {
                this.state.categories = [];
            }
        } catch (error) {
            console.error("Error loading initial data:", error);
            this.notification.add(_t("Failed to load initial data."), { type: 'danger' });
        }
    }

    selectTable(table) {
        if (this.state.selectedTable?.id === table.id) {
            this.state.selectedTable = null;
        } else {
            this.state.selectedTable = table;
        }
    }

    addToCart(menuItem) {
        if (!this.state.selectedTable) {
            this.notification.add(_t("Please select a table first."), { type: 'warning' });
            return;
        }
        const existingLine = this.state.currentOrderLines.find(line => line.menuItemId === menuItem.id);
        if (existingLine) {
            existingLine.qty += 1;
            existingLine.subtotal = existingLine.qty * existingLine.price;
        } else {
            this.state.currentOrderLines.push({
                menuItemId: menuItem.id,
                name: menuItem.name,
                qty: 1,
                price: menuItem.price,
                subtotal: menuItem.price,
            });
        }
        this.computeTotal();
    }

    updateCartQuantity(line, newQty) {
        if (newQty <= 0) {
            this.state.currentOrderLines = this.state.currentOrderLines.filter(l => l.menuItemId !== line.menuItemId);
        } else {
            const lineToUpdate = this.state.currentOrderLines.find(l => l.menuItemId === line.menuItemId);
            if (lineToUpdate) {
                lineToUpdate.qty = newQty;
                lineToUpdate.subtotal = newQty * lineToUpdate.price;
            }
        }
        this.computeTotal();
    }

    computeTotal() {
        this.state.currentTotal = this.state.currentOrderLines.reduce((sum, line) => sum + line.subtotal, 0);
    }

    async sendOrderToKitchen() {
        if (!this.state.selectedTable || this.state.currentOrderLines.length === 0) {
            this.notification.add(_t("Please select a table and add items to the order."), { type: 'warning' });
            return;
        }

        this.state.isLoading = true;
        const orderLinesForRpc = this.state.currentOrderLines.map(line => ({
            product_id: line.menuItemId,
            qty: line.qty,
        }));

        try {
            const newOrderId = await this.orm.call(
                "restaurant_management.order",
                "create_order_from_ui",
                [],
                {
                    table_id: this.state.selectedTable.id,
                    order_lines_data: orderLinesForRpc,
                }
            );

            if (newOrderId) {
                this.notification.add(_t("Order sent successfully!"), { type: 'success' });
                this.state.selectedTable = null;
                this.state.currentOrderLines = [];
                this.state.currentTotal = 0;
            } else {
                throw new Error("Order creation returned no ID.");
            }
        } catch (error) {
            console.error("Error sending order:", error);
            const message = error.data?.message || _t("Failed to send order. Please try again.");
            this.notification.add(message, { type: 'danger' });
        } finally {
            this.state.isLoading = false;
        }
    }
}
