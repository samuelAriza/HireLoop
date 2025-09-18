'''
Mixins
'''

class BootstrapStylingMixin():
    '''
    Mixin that applies Bootstrap form-control class to all fields
    '''
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class':'form-control'})