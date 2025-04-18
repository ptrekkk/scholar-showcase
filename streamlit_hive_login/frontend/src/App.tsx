import { useEffect, useState } from "react"
import {
  Streamlit,
  withStreamlitConnection,
  ComponentProps
} from "streamlit-component-lib"
import "./App.css"

const HiveLogin = (props: ComponentProps) => {
  const [username, setUsername] = useState("")
  const theme = props.theme

  useEffect(() => {
    Streamlit.setComponentReady()
    Streamlit.setFrameHeight()
  }, [])

  const onLogin = () => {
    if (!username) return

    // @ts-ignore
    if (typeof window.hive_keychain === 'undefined') {
      Streamlit.setComponentValue({
        success: false,
        message: "Hive Keychain SDK not loaded.",
        username: username,
        ts: null,
        sig: null,
      })
      return
    }

    const ts = Date.now()
    const message = username + ts

    // @ts-ignore
    window.hive_keychain.requestSignBuffer(username, message, 'Posting', (response) => {
      if (response.success) {
        Streamlit.setComponentValue({
          success: true,
          message: "Message signed successfully!",
          username: username,
          ts: ts,
          sig: response.result,
        })
      } else {
        Streamlit.setComponentValue({
          success: false,
          message: "Error in signing message.",
          username: username,
          ts: ts,
          sig: null,
        })
      }
    })
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      onLogin()
    }
  }

  return (
    <div className={`container ${theme?.base === 'dark' ? 'dark' : 'light'}`}>
      <input
        className="username-input"
        placeholder="Hive username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        onKeyDown={handleKeyDown}
      />
      <button className="login-button" onClick={onLogin} />
    </div>
  )
}

export default withStreamlitConnection(HiveLogin)
