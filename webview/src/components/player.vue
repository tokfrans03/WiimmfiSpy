<template>
  <div>

    <v-container class="px-4">
      <v-row align="start" no-gutters style="height: 150px">
        <v-col> 
            <p>
            </p>
        </v-col>
        <v-spacer></v-spacer>
        <v-col> 
            {{vp}}
        </v-col>
        <v-col cols="auto"> 
            {{name}}
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
export default {
  name: "player",
  props: {
    name: String,
    fc: String,
    vp: Number,
  },
  methods: {},
};
</script>

<style>
</style>