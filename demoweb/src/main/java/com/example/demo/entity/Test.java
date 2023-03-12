package com.example.demo.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.Getter;

@Data
@Entity
@Table(name = "test")
public class Test {

    @Id
    @Column(name = "uid",nullable= false)
    private Integer id;

    @Column(name = "abc",length = 45,nullable = false)
    private String abc;

    @Column(name = "abcd",length = 45,nullable = false)
    private String abcd;

    // getters and setters
}
