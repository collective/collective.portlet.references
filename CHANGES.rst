Changelog
=========

1.0.1 (unreleased)
------------------

- Register as z3c.autoinclude.plugin for plone.
  [maurits]

- Moved to github:
  https://github.com/collective/collective.portlet.references
  [maurits]


1.0 - (9 June 2008)
-------------------

- Use /view for e.g. images/files (using view_url from
  plone_context_state).
  [maurits]

- Place references without a workflow in the list of visible items.
  [maurits]

- Do not show portlet for anonymous.  [maurits]

- Only report relations 'isReferencing' (from plone.app.linkintegrity)
  and 'relatesTo' (relatedItems) and not for example 'translationOf'
  from LinguaPlone.  [maurits]

- Added French and Spanish locales.  [maurits]

- Removed the edit/add forms.  [maurits]

- Split the references into (in)visible links in the text and related
  items.  [maurits]

- Show review state title and use state coloring.  [maurits]

- Only display when there are references.  [maurits]

- Initial release

