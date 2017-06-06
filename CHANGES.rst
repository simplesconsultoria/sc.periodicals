Changelog
---------

1.0b2 (unreleased)
^^^^^^^^^^^^^^^^^^

- Remove dependency on five.grok (closes `#11`_).
  [rodfersou]

- Remove hard dependency on plone.app.referenceablebehavior as Archetypes is no longer the default framework in Plone 5.
  Under Plone < 5.0 you should now explicitly add it to the `eggs` part of your buildout configuration to avoid issues while upgrading.
  [hvelarde]

- Drop support for Python 2.6 and Plone 4.2.
  [hvelarde]


1.0b1 (2013-09-02)
^^^^^^^^^^^^^^^^^^

- Registry resource folder. [cleberjsantos]


1.0a3 (2013-05-03)
^^^^^^^^^^^^^^^^^^

- Fix translation of weekdays on header viewlet; we were getting 'day' instead
  of 'weekday' from publication date. [hvelarde]


1.0a2 (2013-05-03)
^^^^^^^^^^^^^^^^^^

- Use effective date instead of creation date for getting the latest
  periodical; still not optimal, but it probably will work better. [hvelarde]

- Publication date format was localized and is now configurable via the
  viewlet template (closes `#6`_). [hvelarde]

- A new rich text field was added to the Periodical content type. [hvelarde]

- Use 'preview' scale instead of 'mini' for image size in view template.
  [hvelarde]

- Remove dependency on unittest2 and fix package dependencies; tests could
  fail on Python 2.6; you have been warned. [hvelarde]

- Update Brazilian Portuguese and Spanish translations. [hvelarde]

- Remove unassociated template periodicals_list. [hvelarde]

- Do not allow discussion by default in Periodical content type. [hvelarde]

- Added image_thumb and tag methods to the content type allowing it to be
  listed on folder_summary_view. [ericof]


1.0a1 (2013-03-13)
^^^^^^^^^^^^^^^^^^^^

- Initial release.

.. _`#6`: https://github.com/simplesconsultoria/sc.periodicals/issues/6
.. _`#11`: https://github.com/simplesconsultoria/sc.periodicals/issues/11
