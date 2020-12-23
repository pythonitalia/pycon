from i18n.fields import I18nCharField, I18nTextField
from i18n.forms import I18nTextarea, I18nTextInput


def test_i18n_textarea():
    widget = I18nTextarea(
        locales=[("en", "English"), ("it", "Italian")], field=I18nTextField()
    )
    output = widget.render("msg", "value")

    assert (
        output
        == """<div class="i18n-form-group"><div>
  <label style="width: auto; margin-right: 20px;">
    <strong style="display:block; margin-bottom: 10px;">English:</strong>\n
    <textarea name="msg_0" cols="40" rows="10" lang="en">
</textarea>\n
  </label>
</div><div>
  <label style="width: auto; margin-right: 20px;">
    <strong style="display:block; margin-bottom: 10px;">Italian:</strong>\n
    <textarea name="msg_1" cols="40" rows="10" lang="it">
value</textarea>\n
  </label>
</div></div>"""
    )


def test_i18n_textinput():
    widget = I18nTextInput(
        locales=[("en", "English"), ("it", "Italian")], field=I18nCharField()
    )
    output = widget.render("msg", "value")

    assert (
        output
        == """<div class="i18n-form-group"><div>
  <label style="width: auto; margin-right: 20px;">
    <strong style="display:block; margin-bottom: 10px;">English:</strong>\n
    <input type="text" name="msg_0" lang="en">\n
  </label>\n</div><div>
  <label style="width: auto; margin-right: 20px;">
    <strong style="display:block; margin-bottom: 10px;">Italian:</strong>\n
    <input type="text" name="msg_1" value="value" lang="it">\n
  </label>
</div></div>"""
    )
