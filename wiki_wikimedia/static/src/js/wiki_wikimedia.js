openerp.wiki_wikimedia = function (openerp) {
    openerp.wiki.FieldWikiReadonly = openerp.web.page.FieldCharReadonly.extend({
        set_value: function (value) {
            var show_value = InstaView.convert(value || '');
            this.$element.find('div').html(show_value);
            return show_value;
        }
    });
};
