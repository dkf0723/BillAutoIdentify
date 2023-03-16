package com.example.demo.Repository;

import com.example.demo.entity.Test;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface TestRepository extends JpaRepository<Test, Integer> {

//    Optional<Test> findById(Integer id);

}
