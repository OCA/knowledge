To reference records in pages you must set rules. Document rules let you
define which models can be referenced and which field will be used as identifier.
For example, we could create a rule named 'RULE1' that allows you to reference
res.partner records based on its 'ref' field.

When editing a document page add elements like ${XYZ} where X is the rule's identifier,
Y is a separator and Z is the value of the record's field we will search.
Now, when viewing the document, it will link directly to the record.
Also, the name will be parsed as the display name.
