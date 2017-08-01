/*
 * Licensed to the Apache Software Foundation (ASF) under one or more contributor license
 * agreements. See the NOTICE file distributed with this work for additional information regarding
 * copyright ownership. The ASF licenses this file to You under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance with the License. You may obtain a
 * copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License
 * is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 * or implied. See the License for the specific language governing permissions and limitations under
 * the License.
 */
package io.pivotal.workshop.directory;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

public class DirectoryRepository {
  private List<Student> directory = new ArrayList<Student>() {{
    add(new Student("john", "john@pivotal.io"));
    add(new Student("jane", "jane@pivotal.io"));
  }};

  public List<Student> getDirectory() {
    return directory;
  }

  public ResponseEntity<? extends Object> searchByEmail(String email) {
    Optional<Student> result = findByEmail(email);

    return result.<ResponseEntity<? extends Object>>map(ResponseEntity::ok)
        .orElseGet(() -> ResponseEntity.status(HttpStatus.NOT_FOUND).body("{}"));

  }

  private Optional<Student> findByEmail(String email) {
    return directory.stream().filter(s -> s.getEmail().equalsIgnoreCase(email)).findFirst();
  }
}
