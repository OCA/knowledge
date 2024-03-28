* Remove `FormRenderer` patch, convert `AttachmentPreviewWidget` into a component instead.
* Remove `BinaryField` patch, convert preview button into a component instead.
* Don't use `bus.trigger("open_attachment_preview", ...)` to open viewer from an attachment; there
  must be a smoother way.
* Binary fields only have an external preview button. Also add inline preview; stub code is already
  there.
* Add tests to ensure preview & open buttons are rendered in attachment cards.
* Add JS tests to ensure preview & open buttons work as expected (display viewer / open url).
