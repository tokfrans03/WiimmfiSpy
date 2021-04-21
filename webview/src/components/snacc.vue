<template>
  <v-snackbar v-model="show" :color="color">
    {{ message }}

    <template v-slot:action="{ attrs }">
      <v-btn text v-bind="attrs" @click="show = false"> Stäng </v-btn>
    </template>
  </v-snackbar>
</template>

<script lang="ts">
export default {
  name: "snacc",
  props: {
    show: Boolean,
    color: String,
    message: String,
  },
};
</script>