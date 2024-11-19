# Real-time Audio-Communication-Simulation
This project is a **real-time audio communication system** leveraging advanced networking concepts, cryptography, and multithreading. It enables secure, low-latency audio communication between two clients, using **AES encryption** for data security and **multithreaded buffering** for smooth audio transmission and playback.

`It involved designing a multi-threaded simulation of real-time audio communication that efficiently fills and empties a shared buffer simultaneously from either end. The recording thread captures audio and stores it in the buffer, while the playback thread retrieves and plays the audio. This process involved complex thread synchronization to ensure data integrity and smooth operation, providing hands-on experience with threading models and buffer management in a real-time system. `


#### **1. Networking:**
- **Sockets**: Used for establishing a connection between the server and the client.  
  - The server listens for incoming connections and routes audio data between clients.
  - Clients connect using the server's IP address and port.
- **Data Transmission**:
  - A custom protocol with headers specifies the size of incoming data packets, enabling the efficient and complete transfer of audio.

#### **2. Audio Processing:**
- **`sounddevice` Library**:
  - Captures audio input from the microphone and plays back received audio.
  - The system uses `Stream` objects for seamless real-time recording and playback at a sample rate of **44.1 kHz**, which is CD quality.
- **Buffer Management**:
  - **Shared Buffer**:
    - Manages recorded audio using circular buffering to prevent data loss or overflow.
    - Implements producer-consumer threading models for recording, transmitting, receiving, and playing audio.

#### **3. Cryptography:**
- **AES Encryption (Advanced Encryption Standard)**:
  - Secures transmitted audio using **CBC mode** (Cipher Block Chaining) with padding.
  - **IV (Initialization Vector)** ensures encryption randomness for each transmission, making it resistant to attacks.
  - Custom encryption and decryption routines ensure real-time encryption while maintaining low latency.

#### **4. Multithreading:**
- The project employs **four separate threads**:
  1. **Recorder**: Captures audio and pushes it into a buffer.
  2. **Transmitter**: Encrypts and sends audio data from the buffer to the recipient.
  3. **Receiver**: Receives encrypted audio from the sender, decrypts it, and pushes it into another buffer.
  4. **Player**: Fetches audio from the buffer and plays it.

#### **5. Server-Client Architecture:**
- **Server**:
  - Maintains a dictionary of connected clients and their intended recipients.
  - Acts as a mediator to match clients for communication.
  - Ensures no busy client is interrupted by another connection request.
- **Client**:
  - Handles the transmission and reception of audio while maintaining seamless playback.

#### **6. Thread Synchronization:**
- **`Condition` Objects**:
  - Used for coordinating access to shared buffers between threads.
  - Ensure that audio playback and transmission happen only when sufficient data is available.

#### **7. Error Handling and Robustness:**
- Graceful handling of common issues:
  - **BrokenPipeError** and **ConnectionResetError** are addressed to handle abrupt disconnections.
  - **Timeouts** ensure the system does not hang indefinitely during transmission or reception.

#### **8. Scalability:**
- The project supports the addition of multiple clients by maintaining:
  - A shared client registry.
  - Separate threads for each connection.
