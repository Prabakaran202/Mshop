package com.mshop.app

import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import okhttp3.*
import org.json.JSONObject

class MainActivity : AppCompatActivity() {
    private lateinit var webSocket: WebSocket
    private val messages = mutableListOf<String>()
    private lateinit var adapter: ChatAdapter

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val recyclerView = findViewById<RecyclerView>(R.id.chatRecyclerView)
        val messageInput = findViewById<EditText>(R.id.messageInput)
        val sendButton = findViewById<Button>(R.id.sendButton)

        adapter = ChatAdapter(messages)
        recyclerView.layoutManager = LinearLayoutManager(this)
        recyclerView.adapter = adapter

        // Termux FastAPI server-odu inaikka WebSocket (User 1001 aaga hardcode seiyappattullathu)
        val client = OkHttpClient()
        val request = Request.Builder().url("ws://127.0.0.1:8000/ws/chat/1001").build()
        
        webSocket = client.newWebSocket(request, object : WebSocketListener() {
            override fun onMessage(webSocket: WebSocket, text: String) {
                runOnUiThread {
                    try {
                        val json = JSONObject(text)
                        
                        // Normal chat message
                        if (json.has("message_text")) {
                            messages.add("${json.getString("user_id")}: ${json.getString("message_text")}")
                        }
                        // Inventory auto-parse message
                        else if (json.has("new_inventory")) {
                            val inv = json.getJSONObject("new_inventory")
                            messages.add("✅ New Item Added (ID: ${inv.getInt("inventory_id")})")
                        }
                        
                        adapter.notifyItemInserted(messages.size - 1)
                        recyclerView.scrollToPosition(messages.size - 1)
                    } catch (e: Exception) {
                        Log.e("Mshop", "Parse error", e)
                    }
                }
            }
            
            override fun onFailure(webSocket: WebSocket, t: Throwable, response: Response?) {
                runOnUiThread {
                    messages.add("⚠️ Server Connection Failed: Start Termux Server")
                    adapter.notifyDataSetChanged()
                }
            }
        })

        sendButton.setOnClickListener {
            val text = messageInput.text.toString()
            if (text.isNotEmpty()) {
                webSocket.send(text) // Backend-kku message anuppugirathu
                messageInput.text.clear()
            }
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        webSocket.close(1000, "App closed")
    }

    // RecyclerView-kkaana Simple Adapter
    class ChatAdapter(private val messages: List<String>) : RecyclerView.Adapter<ChatAdapter.ViewHolder>() {
        class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
            val textView: TextView = view.findViewById(android.R.id.text1)
        }
        override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
            val view = LayoutInflater.from(parent.context)
                .inflate(android.R.layout.simple_list_item_1, parent, false)
            return ViewHolder(view)
        }
        override fun onBindViewHolder(holder: ViewHolder, position: Int) {
            holder.textView.text = messages[position]
        }
        override fun getItemCount() = messages.size
    }
}
