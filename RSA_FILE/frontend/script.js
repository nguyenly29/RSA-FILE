async function signFile() {
    const file = document.getElementById("fileToSign").files[0];
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("/sign", {
        method: "POST",
        body: formData
    });
    const data = await res.json();
    document.getElementById("signResult").textContent = JSON.stringify(data, null, 2);
    document.getElementById("publicKey").value = data.public_key;
    document.getElementById("signature").value = data.signature;
}

async function verifyFile() {
    const file = document.getElementById("fileToVerify").files[0];
    const formData = new FormData();
    formData.append("file", file);
    formData.append("public_key", document.getElementById("publicKey").value);
    formData.append("signature", document.getElementById("signature").value);

    const res = await fetch("/verify", {
        method: "POST",
        body: formData
    });
    const data = await res.json();
    document.getElementById("verifyResult").textContent = JSON.stringify(data, null, 2);
}