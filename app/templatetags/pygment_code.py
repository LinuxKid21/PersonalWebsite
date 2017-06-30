from django import template
from django.template import Context
register = template.Library()

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter


class PygmentCodeNode(template.Node):
    def __init__(self, content, code_language):
        self.content = content
        self.code_language = code_language

    def render(self, context):
        lineCount = self.content.count('\n')
        hideLines = ''
        if(lineCount > 5):
            hideLines = '<button class="hide-lines-button"> toggle line numbers </button>'
        
        # return the highlighted code with buttons which allow easy selection
        return '<div class="highlight-container">' +\
        hideLines+\
        highlight(self.content, get_lexer_by_name(self.code_language, stripall=True), HtmlFormatter(linenos='inline')) +\
        '</div>'

@register.tag
def pygment_code(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, code_language = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("pygment_code tag requires exactly one argument")
    
    if not (code_language[0] == code_language[-1] and code_language[0] in ('"', "'")):
        raise template.TemplateSyntaxError("pygment_code tag's argument should be in quotes")

    #strip the quotation marks
    code_language = code_language[1:-1]

    nodelist = parser.parse(('endpygment_code',))
    parser.delete_first_token()
    return PygmentCodeNode(nodelist.render(Context()), code_language)
