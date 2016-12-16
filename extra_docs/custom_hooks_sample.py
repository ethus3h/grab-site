"""
This is a sample script that can be passed to grab-site --custom-hooks=.
It drops http:// URLs before they can be queued, and it aborts responses
that have a Content-Type: that starts with 'audio/'
"""

def has_content_type_text(response_info):
	try:
		t = list(p for p in response_info["fields"] if p[0] == "Content-Type")[0][1]
		return t.lower().startswith("text/")
	except (IndexError, ValueError):
		return False

handle_pre_response_grabsite = wpull_hook.callbacks.handle_pre_response
def handle_pre_response(url_info, url_record, response_info):
	url = url_info['url']
	if not has_content_type_text(response_info):
		print("Dropping %s because it has non-text mime type" % url)
		return wpull_hook.actions.FINISH
	return handle_pre_response_grabsite(url_info, url_record, response_info)

wpull_hook.callbacks.handle_pre_response = handle_pre_response
