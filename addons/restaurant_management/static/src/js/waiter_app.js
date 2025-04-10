/** @odoo-module **/

import { registry } from "@web/core/registry";
import { WaiterOrderScreen } from "./waiter_order_screen";

registry.category("actions").add("restaurant_management.WaiterOrderScreen", WaiterOrderScreen);
