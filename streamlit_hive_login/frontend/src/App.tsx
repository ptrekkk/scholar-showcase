import { useEffect, useState, useCallback } from "react";
import {
  Streamlit,
  withStreamlitConnection,
  ComponentProps
} from "streamlit-component-lib";
import { KeychainKeyTypes, KeychainSDK, Login } from "keychain-sdk";   // NEW
import "./App.css";

const keychain = new KeychainSDK(window as any);      // NEW

const HiveLogin = (props: ComponentProps) => {
  const [username, setUsername] = useState("");

  // ───────────── 1. Ask Keychain (extension *or* mobile) to initialise itself
  useEffect(() => {
    // The call is safe even if Keychain is not installed.
    console.log("TEST");
    (window as any).hive_keychain?.requestHandshake?.(() => {});
    Streamlit.setComponentReady();
    Streamlit.setFrameHeight();
  }, []);

  // ───────────── 2. Main login handler (now async/await + SDK)
  const onLogin = useCallback(async () => {
    if (!username) return;

    /* 2-a Detect Keychain (desktop or mobile) */
    const hasKC = await keychain.isKeychainInstalled();  // SDK helper
    if (!hasKC) {
      Streamlit.setComponentValue({
        success: false,
        message: "Hive Keychain not detected.",
        username,
        ts: null,
        sig: null,
      });
      return;
    }

    /* 2-b Build and send the login (= signBuffer) request */
    const ts = Date.now().toString();
    const payload: Login = {
      username,
      message: ts,
      method: KeychainKeyTypes.posting,
      title: "Login",
    };

    try {
      const res = await keychain.login(payload);        // SDK helper
      Streamlit.setComponentValue({
        success: res.success,
        message: res.success ? "Message signed!" : res.message,
        username,
        ts,
        sig: res.result ?? null,
      });
    } catch (err: any) {
      Streamlit.setComponentValue({
        success: false,
        message: err?.message || "Keychain error",
        username,
        ts,
        sig: null,
      });
    }
  }, [username]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") onLogin();
  };

  /* 2-c UI stays unchanged */
  const theme = props.theme;
  return (
    <div className={`container ${theme?.base === "dark" ? "dark" : "light"}`}>
      <input
        className="username-input"
        placeholder="Hive username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        onKeyDown={handleKeyDown}
      />
      <button className="login-button" onClick={onLogin} />
    </div>
  );
};

export default withStreamlitConnection(HiveLogin);
