package io.github.gsalesc.user_service.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import io.github.gsalesc.user_service.model.User;

public interface UserRepository extends JpaRepository<User, Integer>{

}
