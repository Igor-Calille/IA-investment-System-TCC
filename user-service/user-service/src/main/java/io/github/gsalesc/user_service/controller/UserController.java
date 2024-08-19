package io.github.gsalesc.user_service.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import io.github.gsalesc.user_service.model.User;

@RestController
@RequestMapping("/api/user")
public class UserController {

	@PostMapping("/new")
	public void newUser(User u) {
		
	}
	
	@GetMapping
	public String getUser() {
		return "";
	}
	
	@PatchMapping("/{user_id}")
	public void editUser(@PathVariable int user_id, User u) {
		
	}
}
