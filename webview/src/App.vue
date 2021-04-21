<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <div class="d-flex align-center">
        <h1>WiimmfiSpy</h1>
      </div>
      <v-spacer></v-spacer>
      <v-switch
        class="pt-5"
        @change="wsswitch()"
        color="success"
        label="webSocket"
        v-model="ws"
      ></v-switch>
      <v-btn class="ml-4" color="error" @click="delRooms()"
        >Remove all rooms</v-btn
      >
    </v-app-bar>
    <v-snackbar v-model="show" :color="color">
      {{ message }}

      <template v-slot:action="{ attrs }">
        <v-btn text v-bind="attrs" @click="show = false"> Stäng </v-btn>
      </template>
    </v-snackbar>

    <v-main>
      <div>
        <v-card
          class="mx-auto my-4 py-4 elevation-10"
          max-width="900"
          min-width="300"
        >
          <!-- <player
            v-for="(player, index) in players"
            :key="index"
            :name="player.name"
            :fc="player.fc"
            :vp="player.vp"
          /> -->
          <div v-if="room">
            <v-simple-table dense>
              <template v-slot:default>
                <thead>
                  <p class="pl-4">{{ room.players.length }} Players in room</p>
                  <p class="pl-4">{{ round(avgVR, 1) }} avg VR</p>
                  <tr>
                    <th class="text-left">CC</th>
                    <th class="text-left">Track</th>
                    <th class="text-left">Since start</th>
                    <th class="text-left">ID</th>
                    <th class="text-left">Type</th>
                    <th class="text-left">Match#</th>
                    <th class="text-left">Age</th>
                    <th class="text-left">(Lag)</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>{{ room.metadata.cc }}</td>
                    <td>{{ room.metadata.Track }}</td>
                    <td>{{ room.metadata.duration }}</td>
                    <td>{{ room.metadata.id }}</td>
                    <td>{{ room.metadata.type }}</td>
                    <td>{{ room.metadata.Match }}</td>
                    <td>{{ room.metadata.age }}</td>
                    <td>{{ room.metadata.Lag }}</td>
                  </tr>
                </tbody>
              </template>
            </v-simple-table>
            <v-simple-table dense>
              <template v-slot:default>
                <thead>
                  <tr>
                    <th class="text-left">Friend code</th>
                    <th class="text-left">VR</th>
                    <th class="text-left">Name</th>
                    <th class="text-left">Time</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in room.players" :key="item.name">
                    <td>{{ item.fc }}</td>
                    <td>{{ item.vp }}</td>
                    <td>{{ item.name }}</td>
                    <td>{{ item.time }}</td>
                  </tr>
                </tbody>
              </template>
            </v-simple-table>
          </div>
          <v-form
            v-else
            v-model="valid"
            @submit="requestRoom(roomurl)"
            onSubmit="return false;"
          >
            <v-row>
              <v-col>
                <v-text-field
                  class="mx-4"
                  v-model="roomurl"
                  label="New room/friend url"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="auto">
                <v-btn
                  class="ma-4"
                  color="success"
                  :disabled="!valid"
                  :loading="loading"
                  outlined
                  @click="requestRoom(roomurl)"
                  >Send</v-btn
                >
              </v-col>
            </v-row>
          </v-form>
        </v-card>
      </div>
    </v-main>
  </v-app>
</template>
<script lang="ts">
// import player from "./components/player.vue";
import Vue from "vue";

interface Player {
  name: string;
  vp: number;
  combo: string;
  fc: string;
  time: string;
}

interface metadata {
  id: string;
  age: string;
  type: string;
  cc: string;
  Match: string;
  duration: string;
  Lag: string;
  Track: string;
}

interface Room {
  url: string;
  players?: Player[];
  metadata?: metadata;
}

export default Vue.extend({
  name: "App",
  components: {
    // player
  },
  data: () => ({
    loading: false,
    valid: false,
    show: false,
    message: "",
    color: "",
    url: "localhost:8000",
    websocket: (undefined as unknown) as WebSocket,
    ws: false,
    roomurl: "",
    room: (undefined as unknown) as Room,
    // url: "hahahah",
    // players: [
    // {
    //   name: "boi",
    //   fc: "aadwada",
    //   vp: 9999,
    // },
    // ]
    //
  }),
  mounted() {
    console.log("Hej");
    console.log("Hej");
    console.log("Hej");
    this.showMessage("Hej", "success");
  },
  computed: {
    avgVR: function () {
      let tot_VR = 0;
      this.room.players?.forEach((player: Player) => {
        tot_VR += player.vp;
      });
      let numPlayers = this.room.players?.length;
      if (numPlayers) {
        return tot_VR / numPlayers;
      }
      return 5000;
    },
  },
  methods: {
    round(n: number, d = 0) {
      return Math.round(n * 10 ** d) / 10 ** d;
    },
    setRoom(room: Room) {
      this.room = room;
    },
    wsswitch() {
      if (this.ws) {
        this.websocket = new WebSocket("ws://" + this.url + "/ws");
        this.websocket.onmessage = this.onmsg;
      } else {
        this.websocket.close();
      }
    },
    onmsg(event: { data: string }) {
      let d = JSON.parse(event.data);
      console.log(d);
      if (d.type == "update") {
        this.setRoom(d.message);
      } else {
        console.log("msg");
        this.showMessage(d.message, "success");
      }
    },
    showMessage(message: string, color: string) {
      this.show = true;
      this.message = message;
      this.color = color;
    },
    async requestRoom(url: string) {
      fetch("http://" + this.url + "/room", {
        method: "POST",
        mode: "cors",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url: url }),
      }).then(async (response) =>
        this.showMessage(await response.text(), "success")
      );
    },
    async delRooms() {
      this.room = (undefined as unknown) as Room
      fetch("http://" + this.url + "/room", {
        method: "DELETE",
        mode: "cors",
        headers: {
          "Content-Type": "application/json",
        },
      });
    },
  },
});
</script>

