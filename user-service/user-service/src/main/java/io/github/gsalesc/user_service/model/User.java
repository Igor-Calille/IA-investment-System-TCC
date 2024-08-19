package io.github.gsalesc.user_service.model;

import java.time.LocalDate;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;


@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
public class User {
	private String nome;
	private String email;
	private String CPF;
	private LocalDate dataNascimento;
	private String senha;
}
