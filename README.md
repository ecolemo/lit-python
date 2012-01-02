# lit-python
lit is Language Independent Template engine. lit-python is python implementation.

## lit syntax
### scriptlet
You can use any statements of the script language. It'll be executed.
	<%
		a = 1 + 5
		b = 'Hello World'
	%>
### expression
You can use any expressions of the script language. It'll be evaluated and printed.
	<span class="number"><%= 5 + 5 %></span>
### declaration
	<%!
		import re
	%>
### directive
directive gives special control.
#### extends
lit support template inheritance.

	<%@ extends name="parent_template" %>

#### block
	<%@ block name="header" %>
		<ul class="menu">
			<li>…</li>
			…
		</ul>
	<%@ endblock %>
#### page
specify optional parameters. for example, you can execute lit with RestrictedPython with this:
	<%@ page name="runtime" value="restricted" %>
or you can change template language:
	<%@ page name="language" value="JavaScript" %>

## install
	easy_install lit-python
or
	pip install lit-python

## API usage
	from lit.template import Template
	Template(text=u'blahblah…').render(a=1, b='hello')
	Template(filename='hello', lookup=TemplateLookup(directories=['.', './templates']))
