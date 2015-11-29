from algorithm.strings.utils import uni

class Table(list):
    
    def __init__(self, *args):
        list.__init__(self, args)

    def to_html(self):
        html = ['<table width=100%>']
        if self:
            columns = set()

            for item in self:
                columns.update(item.keys())

            html.append('<tr><td>')
            html.append('</b></td><td><b>'.join(map(uni, columns)))
            html.append('</td></tr>')

            for item in self:
                html.append('<tr><td>')
                html.append('</td><td>'.join(uni(item[column]) if column in item else '<i>undefined</i>' for column in columns))
                html.append('</td></tr>')

        html.append('</table>')
        return ''.join(html)
        
    def _rep_html(self):
        return to_html(self)