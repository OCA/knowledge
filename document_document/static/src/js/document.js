openerp.document_document = function (instance) {
    _t = instance.web._t;
    instance.web.Sidebar.include({
        init : function(){
        	console.log("hello from  document ");
            this._super.apply(this, arguments);
            if (this.getParent().view_type == "form"){
                this.sections.splice(1, 0, { 'name' : 'files', 'label' : _t('Attachment(s)'), });
                this.items['files'] = [];
            }
        },
        on_attachments_loaded: function(attachments) {
            //to display number in name if more then one attachment which has same name.
            var self = this;
            _.chain(attachments)
                 .groupBy(function(attachment) { 
                	 console.log("hello from  document 1 ");
                	 console.log(attachment.name);
                	 return attachment.name
                	 
                 })
                 .each(function(attachment){
                     if(attachment.length > 1)
                         _.map(attachment, function(attachment, i){
                        	 console.log("hello from  document 2 ");
                        	 console.log(i);
                             attachment.name = _.str.sprintf(_t("%s (%s)"), attachment.name, i+4)
                         })
                  })
            self._super(attachments);
        },
    });
};
