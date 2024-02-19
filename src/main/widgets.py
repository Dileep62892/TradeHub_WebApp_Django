from django.forms import widgets
from django.utils.safestring import mark_safe


class CustomListImageFieldWidget(widgets.FileInput):

    '''def render(self, name, value, attrs=None, **kwargs):
        default_html = super().render(name, value, attrs, **kwargs)
        img_html = mark_safe(f'<img src="{value.url}" width="200" height:"200" />')
        return f'{img_html}{default_html}'
    '''
    def render(self, name, value, attrs=None, **kwargs):
        default_html1 = super().render(name, value, attrs, **kwargs)
        img_html1 = ''
        if value and hasattr(value, 'url'):
            img_html1 = mark_safe(f'<img src="{value.url}" width="200" height="150" />')
        return f'{img_html1}{default_html1}'