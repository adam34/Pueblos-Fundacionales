#widgets.py
# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from administrador.models import idioma

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
from django.forms.widgets import Input,SelectMultiple,Widget

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

class MapInput(Input):
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        final_attrs['type'] ='text'
        final_attrs['style'] = 'margin:0 0 10px 0;'
    
        output = [format_html("""<script src="http://maps.google.com/maps/api/js?sensor=true"></script>""")]

        output.append(format_html("""<script src="/static/js/gmaps.js"></script>"""))
        output.append(format_html("""<div class="span8">"""))
        output.append(format_html("""<div class="row">"""))
        output.append(format_html("""<div class='span5'>"""))
        output.append(format_html('<input{0} placeholder="Buscar: Ciudad, Estado, Pais" />', flatatt(final_attrs)))
        output.append(format_html("""</div>"""))
        output.append(format_html("""<div class='span3'>"""))
        output.append(format_html("""<button id='bt-eliminar' class="btn btn-danger">Eliminar marca</button>"""))
        output.append(format_html("""</div>"""))
        output.append(format_html("""</div>"""))
        output.append(format_html("""<div class="row">"""))
        output.append(format_html("""<div id='mapa' class='span10'></div>"""))
        output.append(mark_safe("""<script> map = new GMaps(
            {
            div: '#mapa', 
            height : '400px',
            lat: 24.143131 ,
            lng: -110.31106,
            click: function mapa_click(e) {
                if(map.markers.length>0)
                {
                    map.removeMarkers()
                }
                map.addMarker({
                    lat: e.latLng.lat(),
                    lng: e.latLng.lng()
                });
            },
        });
        $('#id_MAPA').on('keypress',clic);
        function clic(e)
        {
            if(e.charCode==13)
            {
                GMaps.geocode({
                  address: $('#id_MAPA').val(),
                  callback: function(results, status) {
                    if (status == 'OK') {
                      var latlng = results[0].geometry.location;
                      map.setCenter(latlng.lat(), latlng.lng());
                      map.addMarker({
                        lat: latlng.lat(),
                        lng: latlng.lng()
                      });
                    }
                    }
                });
                return false;
            }
        }
        $('#bt-eliminar').on('click',eliminar_marca)
        function eliminar_marca(e)
        {
            if(map.markers.length>0)
            {
                map.removeMarkers()
            }
            return false;
        }
        </script>
        </div>
        </div>"""))
        # if value != '':
        #     # Only add the 'value' attribute if a value is non-empty.
        #     final_attrs['value'] = force_text(self._format_value(value))
        return mark_safe('\n'.join(output))
class AccordionMultipleTextbox(Widget):
    def render(self, name, value, attrs=None):
        if value is None: value = ''
        # output= [mark_safe("""
        # <div class="accordion" id="accordion2">
        #     <div class="accordion-group">
        #         <div class="accordion-heading">
        #             <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseOne">
        #                 Español
        #             </a>
        #         </div>
        #         <div id="collapseOne" class="accordion-body collapse in">
        #             <div class="accordion-inner">
        #                 <textarea> </textarea>
        #             </div>
        #         </div>
        #     </div>
        #     <div class="accordion-group">
        #         <div class="accordion-heading">
        #             <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseTwo">
        #                 Inglés
        #             </a>
        #         </div>
        #         <div id="collapseTwo" class="accordion-body collapse">
        #             <div class="accordion-inner">
        #                 <textarea> </textarea>
        #             </div>
        #         </div>
        #     </div>
        #     <div class="accordion-group">
        #         <div class="accordion-heading">
        #             <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseThree">
        #                 Aléman
        #             </a>
        #         </div>
        #         <div id="collapseThree" class="accordion-body collapse">
        #             <div class="accordion-inner">
        #                 <textarea> </textarea>
        #             </div>
        #         </div>
        #     </div>
        # </div>
        # """)]

        # output= [mark_safe("""
        # <div class='row'>
        #     <div class='span8'>
        #         <ul class="nav nav-tabs" id="myTab">
        #             <li class="active"><a href="#home">Español</a></li>
        #             <li><a href="#profile">Inglés</a></li>
        #             <li><a href="#messages">Aléman</a></li>
        #             <li><a href="#settings">Portugues</a></li>
        #         </ul>

        #         <div class="tab-content">
        #             <div class="tab-pane active" id="home">
        #                 <textarea class='vTextField span12' rows='10'>aaaa</textarea>
        #             </div>
        #             <div class="tab-pane" id="profile">
        #                 <textarea class='vTextField span12' rows='10'>bbbb</textarea>
        #             </div>
        #             <div class="tab-pane" id="messages">
        #                 <textarea class='vTextField span12' rows='10'>cccc</textarea>
        #             </div>
        #             <div class="tab-pane" id="settings">
        #                 <textarea class='vTextField span12' rows='10'>dddd</textarea>
        #             </div>
        #         </div>
        #         <script>
        #         $(function () {
        #             $('#myTab a:first').tab('show');
        #         })
        #         $('#myTab a').click(function (e) {
        #           e.preventDefault();
        #           $(this).tab('show');
        #         })
        #         </script>
        #     </div>
        # </div>
        # """)]
        idiomas=idioma.objects.all()
        output= [mark_safe("""<div class='row'>""")]
        output.append(mark_safe("""<div class='span8'>"""))
        output.append(mark_safe("""<ul class="nav nav-tabs" id="%s_descripcion">""" % (name)))
        output.append(mark_safe("""<li class="active"><a href="#Español">Español</a></li>"""))
        for idiom in idiomas:
            output.append(mark_safe("<li><a href='#"+idiom.NOMBRE+"'>"+idiom.NOMBRE+"</a></li>"))
        output.append(mark_safe("""</ul>"""))
        output.append(mark_safe("""<div class="tab-content">"""))
        output.append(mark_safe("""
                <div class='tab-pane active' id='Español'>
                    <textarea class='vTextField span12' rows='10' placeholder='Descripción en Español'></textarea>
                </div>
            """))
        for idiom in idiomas:
            output.append(mark_safe("""
                    <div class='tab-pane' id='"""+idiom.NOMBRE+"""'>
                        <textarea class='vTextField span12' rows='10' placeholder=' Descripción en """+idiom.NOMBRE+"""'></textarea>
                    </div>
                """))
        output.append(mark_safe("""</div>"""))
        output.append(mark_safe("""
            <script>
                $(function () {
                    $('#%s_descripcion a:first').tab('show');
                })
                $('#%s_descripcion a').click(function (e) {
                  e.preventDefault();
                  $(this).tab('show');
                })
                </script>
            </div>
        </div>
        """ % (name,name)))
        return mark_safe('\n'.join(output))


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