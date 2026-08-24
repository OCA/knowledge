/** @odoo-module **/
/* global QUnit */
/* Copyright 2026 Jarsa
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */

import {parseXml} from "@attachment_preview_xml/xml_viewer.esm";

const CFDI = `<?xml version="1.0" encoding="utf-8"?>
<cfdi:Comprobante xmlns:cfdi="http://www.sat.gob.mx/cfd/4" Total="1073.00">
<!-- emisor --><cfdi:Emisor Rfc="TLU080610C81" Nombre="ETN TURISTAR LUJO"/>
<cfdi:Conceptos><cfdi:Concepto Cantidad="1">Servicios de buses</cfdi:Concepto></cfdi:Conceptos>
</cfdi:Comprobante>`;

QUnit.module("attachment_preview_xml", () => {
    QUnit.test("parseXml builds a hierarchy out of a one-line CFDI", (assert) => {
        const root = parseXml(CFDI);
        assert.strictEqual(root.tag, "cfdi:Comprobante");
        assert.deepEqual(
            root.attrs.map((attr) => attr.name),
            ["xmlns:cfdi", "Total"]
        );
        assert.ok(root.isBranch, "the root node is collapsible");
        assert.deepEqual(
            root.children.map((child) => child.type),
            ["comment", "element", "element"]
        );

        const [comment, emisor, conceptos] = root.children;
        assert.strictEqual(comment.value, "emisor");
        assert.notOk(emisor.isBranch, "an empty node is not collapsible");
        assert.strictEqual(emisor.attrs[1].value, "ETN TURISTAR LUJO");

        const concepto = conceptos.children[0];
        assert.notOk(concepto.isBranch, "a text-only node is not collapsible");
        assert.strictEqual(concepto.text, "Servicios de buses");
    });

    QUnit.test("parseXml rejects malformed XML", (assert) => {
        assert.throws(() => parseXml("<a><b></a>"));
        assert.throws(() => parseXml("not xml at all"));
    });
});
