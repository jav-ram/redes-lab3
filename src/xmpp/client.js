import * as Strophe from 'strophe.js';

const BOSH_SERVICE = '/xmpp-httpbind';
let connection = null;

export const onConnect = (status) => {
    if (status === Strophe.Status.CONNECTING) {
	    console.log('Strophe is connecting.');

    } else if (status === Strophe.Status.CONNFAIL) {
	    console.log('Strophe failed to connect.');

    } else if (status === Strophe.Status.DISCONNECTING) {
	    console.log('Strophe is disconnecting.');

    } else if (status === Strophe.Status.DISCONNECTED) {
	    console.log('Strophe is disconnected.');

    } else if (status === Strophe.Status.CONNECTED) {
	    console.log('Strophe is connected.');
	    console.log('ECHOBOT: Send a message to ' + connection.jid + 
	    ' to talk to me.');

 /*        connection.addHandler(onMessage, null, 'message', null, null,  null); 
        connection.send($pres().tree()); */
    }
}


export const initialize = (jid, password, callback) => {
    connection = new Strophe.Connection(BOSH_SERVICE);

    connection.connect(
        jid,            // jid
        password,       // password
        callback,       // callback
    );
}