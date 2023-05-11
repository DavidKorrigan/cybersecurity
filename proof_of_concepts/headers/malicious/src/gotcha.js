<script type="text/javascript">
	function sendMessage() {
		var request = new XMLHttpRequest();
		request.open("POST", "https://webhook.site/d3329387-67e9-4310-ad63-316adf90b949");

		request.setRequestHeader('Content-type', 'application/json');

		var params = {
			username: "My Webhook Name",
			avatar_url: "",
			content: "The message to send"
		}
		request.send(JSON.stringify(params));
	}
</script>