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
          min-width="100"
        >
          <!-- <player
            v-for="(player, index) in players"
            :key="index"
            :name="player.name"
            :fc="player.fc"
            :vp="player.vp"
          /> -->
          <div v-if="room">
            <v-row no-gutters>
              <v-col>
                <p class="pl-4">{{ room.players.length }} Players in room</p>
              </v-col>
              <v-spacer></v-spacer>
              <v-col>
                <p>{{ round(avgVR, 1) }} avg VR</p>
              </v-col>
            </v-row>
            <v-simple-table dense>
              <template v-slot:default>
                <thead>
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
            <!-- <v-simple-table dense>
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
            </v-simple-table> -->
            <v-data-table
              dense
              hide-default-footer
              :headers="headers"
              :items="room.players"
              :custom-sort="customSort"
              sort-by="time"
            ></v-data-table>
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
  diff?: string;
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
    headers: [
      {
        text: "Friend code",
        align: "start",
        sortable: false,
        value: "fc",
      },
      { text: "VR", value: "vp" },
      { text: "Diff", value: "diff" },
      { text: "Combo", value: "combo" },
      { text: "Name", value: "name" },
      { text: "Time", value: "time" },
    ],
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
    // this.setRoom({
    //   url: "https://wiimmfi.de/stats/mkwx/room/r2779626",
    //   metadata: {
    //     id: "DC26",
    //     age: "4h",
    //     type: "Versus Race",
    //     cc: "150cc",
    //     Match: "80",
    //     duration: "164s",
    //     Track: "GCN DK Mountain (Nintendo)",
    //   },
    //   players: [
    //     {
    //       name: "SAChris",
    //       vp: 9419,
    //       combo: "Dais/Mach",
    //       fc: "0865-0037-7854",
    //       time: "2:25.297",
    //     },
    //     {
    //       name: "Venti",
    //       vp: 9339,
    //       combo: "Funk/Flam",
    //       fc: "3141-3314-4679",
    //       time: "2:27.951",
    //     },
    //     {
    //       name: "Tok1",
    //       vp: 7702,
    //       combo: "Funk/Flam",
    //       fc: "3570-8340-8289",
    //       time: "2:28.714",
    //     },
    //     {
    //       name: "Dylan",
    //       vp: 8455,
    //       combo: "Funk/Flam",
    //       fc: "3484-9301-6865",
    //       time: "2:29.473",
    //     },
    //     {
    //       name: "GTTFODRUNK",
    //       vp: 7766,
    //       combo: "Funk/Flam",
    //       fc: "3184-2889-2509",
    //       time: "2:30.473",
    //     },
    //     {
    //       name: "simi",
    //       vp: 8350,
    //       combo: "Funk/Flam",
    //       fc: "2840-6841-9172",
    //       time: "2:31.473",
    //     },
        
    //   ],
    // });
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
    timeString2ms(a: any, b: number) {
      // time(HH:MM:SS.mss) // optimized
      return (
        (a = a.split(".")), // optimized
        (b = a[1] * 1 || 0), // optimized
        (a = a[0].split(":")),
        b +
          (a[2]
            ? a[0] * 3600 + a[1] * 60 + a[2] * 1
            : a[1]
            ? a[0] * 60 + a[1] * 1
            : a[0] * 1) *
            1e3
      ); // optimized
    },
    customSort: function (items, index, isDesc) {
      items.sort((a, b): any => {
        if (index[0] === "time") {
          if (isDesc[0]) {
            return this.compareTime(b[index], a[index]);
          } else {
            return this.compareTime(a[index], b[index]);
          }
        } else if (index[0] === "vp") {
          console.log(a[index], b[index], index, isDesc)
          if (!isDesc[0]) {
            return a[index] - b[index]
          } else {
            return b[index] - a[index]
          }
        } else {
          if (typeof a[index] !== "undefined") {
            if (!isDesc[0]) {
              return a[index]
                .toLowerCase()
                .localeCompare(b[index].toLowerCase());
            } else {
              
              return b[index]
                .toLowerCase()
                .localeCompare(a[index].toLowerCase());
            }
          }
        }
      });
      return items;
    },
    compareTime(a, b) {
      if (a == "—") return 1;
      if (b == "—") return -1;

      if (this.timeString2ms(a) > this.timeString2ms(b)) return 1;
      return -1;
    },
    compareTimePlayers(a: Player, b: Player) {
      if (a.time == "—") return 1;
      if (b.time == "—") return -1;

      if (this.timeString2ms(a.time) > this.timeString2ms(b.time)) return 1;
      return -1;
    },
    GetVrDiffByTab(winner: number, looser: number) {
      const vr_diff_tab = [
        6598,
        4999,
        3963,
        3233,
        2671,
        2212,
        1819,
        1476, //   0 ..   7
        1168,
        889,
        633,
        395,
        174,
        -34,
        -231,
        -418, //   8 ..  15
        -596,
        -767,
        -931,
        -1090,
        -1243,
        -1392,
        -1536,
        -1676, //  16 ..  23
        -1813,
        -1946,
        -2076,
        -2203,
        -2328,
        -2450,
        -2569,
        -2687, //  24 ..  31
        -2802,
        -2915,
        -3026,
        -3136,
        -3243,
        -3349,
        -3454,
        -3557, //  32 ..  39
        -3658,
        -3759,
        -3857,
        -3955,
        -4051,
        -4147,
        -4241,
        -4334, //  40 ..  47
        -4425,
        -4516,
        -4606,
        -4695,
        -4783,
        -4870,
        -4957,
        -5042, //  48 ..  55
        -5127,
        -5211,
        -5294,
        -5377,
        -5459,
        -5540,
        -5622,
        -5702, //  56 ..  63
        -5783,
        -5863,
        -5942,
        -6022,
        -6101,
        -6180,
        -6259,
        -6338, //  64 ..  71
        -6417,
        -6495,
        -6574,
        -6653,
        -6731,
        -6810,
        -6889,
        -6968, //  72 ..  79
        -7048,
        -7127,
        -7207,
        -7287,
        -7367,
        -7448,
        -7530,
        -7611, //  80 ..  87
        -7693,
        -7776,
        -7860,
        -7944,
        -8029,
        -8114,
        -8201,
        -8288, //  88 ..  95
        -8377,
        -8466,
        -8557,
        -8649,
        -8743,
        -8838,
        -8935,
        -9034, //  96 .. 103
        -9135,
        -9239,
        -9345,
        -9455,
        -9568,
        -9684,
        -9806,
        -9933, // 104 .. 111
      ];

      let diff =  winner - looser;
      if (diff > 6598) return 0;
      if (diff < -9933) return 112;

      const search = diff;
      let i = 0;
      let j = Math.floor(448 / 4 - 1);

      while (i < j) {
        const k = Math.floor((i + j) / 2);
        if (search > vr_diff_tab[k]) j = k - 1;
        else if (search <= vr_diff_tab[k + 1]) i = k + 1;
        else return k + 1;
      }

      return i + 1;
    },
    round(n: number, d = 0) {
      return Math.round(n * 10 ** d) / 10 ** d;
    },
    setRoom(room: Room) {
      this.room = room;
      if (this.room.players.some((player) => player.time != "—")) {
        // someone finished
        let activePlayers = this.room.players.filter(player => player.combo !== "—")
        activePlayers.sort(this.compareTimePlayers)
        activePlayers.forEach((player: Player, i: number) => {
          let pplAhead  = activePlayers.slice(0, i)
          let pplBehind = activePlayers.slice(i+1)
          let diff = 0;

          // console.log(player.name, pplAhead, pplBehind)

          pplAhead.forEach((AheadPlayer: Player) => {
            diff -= this.GetVrDiffByTab(AheadPlayer.vp, player.vp)
          });

          pplBehind.forEach((BehindPlayer: Player) => {
            diff += this.GetVrDiffByTab(player.vp, BehindPlayer.vp)
          });

          player.diff = (diff<0?"":"+") + diff

        });

      }
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
      this.room = (undefined as unknown) as Room;
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

