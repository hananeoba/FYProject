import * as React from "react";

import {
  TouchableOpacity,
  View,
  Text,
  TextInput,
  SafeAreaView,
  StyleSheet,
} from "react-native";

import { useState } from "react";

export const Login = ({ addSubject }) => {
  const [subject, setSubject] = useState(null);
  return (
    <View>
      <SafeAreaView>
        <Text>Email</Text>
        <TextInput style={styles.textinput} onChangeText={setSubject} />
        <Text>Password</Text>
        <TextInput textContentType="password" style={styles.textinput} />
        <TouchableOpacity
          style={styles.button}
          onPress={() => {
            addSubject;
          }}
        >
          <Text>Login</Text>
        </TouchableOpacity>
      </SafeAreaView>
    </View>
  );
};

export default Login;

const styles = StyleSheet.create({
  button: {
    paddingTop: 3,
  },
  textinput: {
    height: 40,
    borderColor: "gray",
    borderWidth: 1,
    width: 300,
  },
});
