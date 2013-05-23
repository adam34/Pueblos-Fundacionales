#widgets.py
from __future__ import unicode_literals


#ESTAS LINEAS DE CODIGO SON PARA DEPURACION
# import pdb
# pdb.set_trace()

from django.contrib.admin.templatetags.admin_static import static
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.forms.util import flatatt
from django.utils.html import conditional_escape, format_html, format_html_join
from itertools import chain
from django.forms import *
from django.forms.widgets import *

class SelectMultipleCustom(SelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
    	# output = super(SelectMultipleCustom, self).render(name,value,attrs,choices)
    	# return output
        if value is None: value = []  
        
        if name=='permissions' or name=='user_permissions':
            var='Permisos'
        elif name =='groups':
            var='Grupos'
        else:
            var=name

        final_attrs = self.build_attrs(attrs, name=name)
        output=[format_html('<select id="searchable-{0}" name="my-select[]" multiple="multiple"{1}>', var,flatatt(final_attrs))]
        options = self.render_options(choices, value)
        if options:
            output.append(options)
        output.append('</select>')
        # import pdb
        # pdb.set_trace()
        output.append(mark_safe("""<script type="text/javascript">$("#searchable-%s").multiSelect({selectableHeader: "<input type='text' id='search-%s' class='span12' autocomplete='off' placeholder='Buscar: %s'>"});</script>""" % (var,var,var)))


        output.append(mark_safe("""<script type="text/javascript">$('#search-%s').quicksearch('.ms-selectable-%s .ms-list .ms-elem-selectable');\
        </script>""" % (var,var)))

        #jquery.multi-select.js
        return mark_safe('\n'.join(output))

    def render_option(self, selected_choices, option_value, option_label):
        option_value = force_text(option_value)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = ''
        return format_html('<option value="{0}"{1}>{2}</option>',
                           option_value,
                           selected_html,
                           force_text(option_label))
    def render_options(self, choices, selected_choices):
        # Normalize to strings.
        selected_choices = set(force_text(v) for v in selected_choices)
        output = []
        for option_value, option_label in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(format_html('<optgroup label="{0}">', force_text(option_value)))
                for option in option_label:
                    output.append(self.render_option(selected_choices, *option))
                output.append('</optgroup>')
            else:
                output.append(self.render_option(selected_choices, option_value, option_label))
        return '\n'.join(output)

# class TextAreaEditor(Textarea):
    
#     def render(self, name, value, attrs=None):
#         if value is None: value = ''

#         final_attrs = self.build_attrs(attrs, name=name)
#         format=flatatt(final_attrs)
#         output=[format_html("""<link rel="stylesheet" href="/static/tinymce/js/tinymce/skins/lightgray/skin.min.css">""")]
#         output.append(format_html("""<script src="/static/tinymce/js/tinymce/tinymce.min.js"></script>"""))
#         output.append(format_html("""<script type="text/javascript">"""))
#         output.append(mark_safe("""tinymce.init({
#             selector: "textarea_%s",
#             theme: "modern",
#             width: 300,
#             height: 300,
#             plugins: [
#                  "advlist autolink link image lists charmap print preview hr anchor pagebreak spellchecker",
#                  "searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking",
#                  "save table contextmenu directionality emoticons template paste textcolor"
#            ],
#            toolbar: "insertfile undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | l      ink image | print preview media fullpage | forecolor backcolor emoticons", 
#            style_formats: [
#                 {title: 'Bold text', inline: 'b'},
#                 {title: 'Red text', inline: 'span', styles: {color: '#ff0000'}},
#                 {title: 'Red header', block: 'h1', styles: {color: '#ff0000'}},
#                 {title: 'Example 1', inline: 'span', classes: 'example1'},
#                 {title: 'Example 2', inline: 'span', classes: 'example2'},
#                 {title: 'Table styles'},
#                 {title: 'Table row 1', selector: 'tr', classes: 'tablerow1'}
#             ]
#             });"""%(name)))
#         output.append(format_html("""</script>"""))
#         output.append(format_html('<textarea{0}>\r\n{1}</textarea>',format,force_text(value)))

#         return mark_safe('\n'.join(output))